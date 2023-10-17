# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import atexit
import asyncio
import json
import os
import pickle
import signal
import socket
import logging
import struct
import sys
from pathlib import Path

try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None

from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone
from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer

# from lino.modlib.linod.tasks import Tasks
from lino.utils.socks import send_through_socket, get_from_socket

logger = logging.getLogger('linod')

# used for debugging, when no 'log' dir exists
# if not logger.handlers:
#     logger.addHandler(logging.StreamHandler())
#     logger.setLevel(logging.INFO)


class LogReceiver(asyncio.Protocol):

    def data_received(self, data: bytes):
        data = pickle.loads(data[4:]) # first four bytes gives the size of the rest of the data
        record = logging.makeLogRecord(data)
        logger.handle(record)

from .utils import log_sock_path, worker_sock_path

class LinodConsumer(AsyncConsumer):

    # tasks: Tasks
    clients = set()

    def remove_socks(self):
        log_sock_path.unlink(True)
        worker_sock_path.unlink(True)

    async def log_server(self, event=None):
        logger.info("Running log server")
        asyncio.ensure_future(self.async_log_server())

    async def async_log_server(self):
        # log.server in lino_runworker
        atexit.register(self.remove_socks)
        loop = asyncio.get_running_loop()
        log_sock_path.unlink(True)
        # server = await loop.create_unix_server(
        #     lambda : LogReceiver(), log_sock_path)
        server = await loop.create_unix_server(LogReceiver, log_sock_path)
        try:
            async with server:
                await server.serve_forever()
        finally:
            log_sock_path.unlink(True)

    async def send_push(self, event):
        # logger.info("Push to %s : %s", user or "everyone", data)
        data = event['data']
        user = event['user_id']
        if user is not None:
            user = settings.SITE.models.users.User.objects.get(pk=user)
        kwargs = dict(
            data=json.dumps(data),
            vapid_private_key=settings.SITE.plugins.notify.vapid_private_key,
            vapid_claims={
                'sub': "mailto:{}".format(settings.SITE.plugins.notify.vapid_admin_email)
            }
        )
        if user is None:
            subs = settings.SITE.models.notify.Subscription.objects.all()
        else:
            subs = settings.SITE.models.notify.Subscription.objects.filter(user=user)
        for sub in subs:
            sub_info = {
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            }
            try:
                req = webpush(subscription_info=sub_info, **kwargs)
            except WebPushException as e:
                if e.response.status_code == 410:
                    sub.delete()
                else:
                    raise e

    async def run_system_tasks(self, event: dict):
        # run.system.tasks in lino_runworker
        asyncio.ensure_future(self._run_system_tasks())

    async def _run_system_tasks(self):
        logger.info("Run background jobs (system tasks)")
        # self.tasks = tasks = Tasks()
        # await database_sync_to_async(tasks.setup)()
        ar = settings.SITE.login()
        while True:
            # asyncio.ensure_future
            next_dt = await settings.SITE.models.linod.JobRule.run_them_all(ar)
            # next_dt = await database_sync_to_async(tasks.run)()
            # if not next_dt:
            #     break
            # if next_dt is True:
            #     continue
            if (to_sleep := (next_dt - timezone.now()).total_seconds()) <= 0:
                continue
            # logger.info(f"next system tasks run: {next_dt}")
            await asyncio.sleep(to_sleep)

    async def dev_worker(self, event: dict):
        # dev.worker in lino_runworker
        # worker_sock = str(worker_sock_path)

        def add_client(sock: socket.socket) -> None:
            self.clients.add(get_from_socket(sock))
            sock.close()

        def remove_client(sock: socket.socket, close: bool = True) -> None:
            self.clients.discard(get_from_socket(sock))
            if close:
                sock.close()

        def client_exists(sock: socket.socket) -> None:
            if get_from_socket(sock) in self.clients:
                send_through_socket(sock, b'true')
            else:
                send_through_socket(sock, b'false')
            handle_msg(sock)

        def process_remove_get(sock: socket.socket) -> None:
            remove_client(sock, False)
            data = pickle.dumps({'clients': len(self.clients), 'pid': os.getpid()})
            send_through_socket(sock, data)
            sock.close()

        SIGNALS = {
            b'add': add_client,
            b'exists': client_exists,
            b'remove': remove_client,
            b'remove_get': process_remove_get,
            b'close': lambda sock: sock.close()
        }

        def handle_msg(client_sock: socket.socket) -> None:
            msg = get_from_socket(client_sock)
            if msg not in SIGNALS:
                send_through_socket(client_sock, b"Invalid signal!")
                client_sock.close()
            else:
                SIGNALS[msg](client_sock)

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                worker_sock_path.unlink(True)
                sock.bind(str(worker_sock_path))
                sock.listen(5)
                while True:
                    client_sock, _ = sock.accept()
                    handle_msg(client_sock)
        finally:
            worker_sock_path.unlink(True)

    async def job_list(self, event):
        async def do():
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sockd = str(settings.SITE.site_dir / 'sockd')
                sock.connect(sockd)
                jobs = await database_sync_to_async(self.tasks.status)()
                data = pickle.dumps(jobs)
                await asyncio.sleep(1)
                send_through_socket(sock, data)
        asyncio.ensure_future(do())
