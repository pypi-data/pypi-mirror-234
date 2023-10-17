# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# import asyncio
# import os
# import pickle
# import signal
# import socket
# import sys
# import time
#
# from django.conf import settings
from django.core.management import execute_from_command_line as django_execute_from_command_line
# from pathlib import Path
# from subprocess import Popen, PIPE, DEVNULL
#
# from lino.utils.socks import send_through_socket, get_from_socket
#
# sock = None
#
# try:
#     worker_sock_file = settings.SITE.site_dir / 'worker_sock'
#     log_sock_file = settings.SITE.site_dir / 'log_sock'
# except:
#     pass
#
# CATCHED_EXCEPTIONS = (FileNotFoundError, ConnectionRefusedError)
#
# DEFAULT_TIMEOUT = 1
#
# SKIP_COMMANDS = [
#     'lino_runworker',
#     'runworker',
#     'linod',
#     'help',
#     'run',
#     'install',
#     'dump_settings'
# ]
#
# SKIP_FLAGS = [
#     '--help',
#     '-h'
# ]
#
# SKIP_ARG = SKIP_COMMANDS + SKIP_FLAGS
#
#
# def get_pid() -> bytes:
#     return str(os.getpid()).encode()
#
#
# def get_socket() -> socket.socket:
#     sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     try:
#         sock.connect(str(worker_sock_file))
#     except CATCHED_EXCEPTIONS as e:
#         raise ConnectionRefusedError(
#             "Failed to connect to {} ({})".format(worker_sock_file, e))
#     return sock
#
#
# STDIO = dict(stdout=PIPE, stderr=PIPE, stdin=DEVNULL)
#
#
# def check_and_start_linod(argv=None):
#     if argv:
#         for c in SKIP_ARG:
#             if c in argv:
#                 return
#
#     def add_client():
#         global sock
#         sock = get_socket()
#         send_through_socket(sock, b'add')
#         send_through_socket(sock, get_pid())
#         sock.close()
#
#     if worker_sock_file.exists():
#         add_client()
#         return
#     if log_sock_file.exists():
#         return
#
#     sys.stdout.write("Run worker process ...\n")
#     from lino.modlib.linod.utils import LINOD
#     from channels.layers import get_channel_layer
#     p = Popen(['python', 'manage.py', 'lino_runworker', "--skip-system-tasks"], start_new_session=True, **STDIO)
#     channel_layer = get_channel_layer()
#
#     async def start_worker_processes():
#         await asyncio.sleep(DEFAULT_TIMEOUT)
#         await channel_layer.send(LINOD, {'type': 'dev.worker'})
#         await asyncio.sleep(DEFAULT_TIMEOUT)
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(start_worker_processes())
#
#     def try_add_client(count=0):
#         try:
#             add_client()
#         except (FileNotFoundError, ConnectionRefusedError):
#             if count <= 10:
#                 sys.stdout.write(f'Waiting for worker process: {count} seconds\n')
#                 time.sleep(DEFAULT_TIMEOUT)
#                 try_add_client(count + 1)
#             else:
#                 out, err = p.communicate(1)
#                 raise Exception(err.decode())
#
#     try_add_client()
#
#
# def check_and_start_utility(argv=None):
#     if settings.SITE.use_linod:
#         check_and_start_linod(argv)
#
#
# def stop_utility(argv=None):
#     global sock
#     if sock is not None:
#         sock = get_socket()
#         send_through_socket(sock, b'exists')
#         send_through_socket(sock, get_pid())
#         if get_from_socket(sock) == b'true':
#             send_through_socket(sock, b'remove_get')
#             send_through_socket(sock, get_pid())
#             data = pickle.loads(get_from_socket(sock))
#             sock.close()
#             if data['clients'] == 0:
#                 sys.stdout.write('Terminate worker process ...\n')
#                 os.kill(data['pid'], signal.SIGKILL)
#                 worker_sock_file.unlink(True)
#                 log_sock_file.unlink(True)
#         else:
#             send_through_socket(sock, b'close')
#             sock.close()


def execute_from_command_line(argv=None):
    django_execute_from_command_line(argv)
