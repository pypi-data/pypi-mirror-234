# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import sys
import socket
import pickle
from django.conf import settings
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from lino.modlib.linod.utils import LINOD
from lino.utils.socks import get_from_socket, send_through_socket


class Command(BaseCommand):
    help = """Get system tasks status."""

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', help="Show the tasks status without running them.",
            action='store_true', default=False)

    def handle(self, *args, **options):
        if not settings.SITE.use_linod:
            sys.stdout.write("This site does not use linod.\n")
            return

        if options.get('dry_run'):
            if not (settings.SITE.site_dir / 'log_sock').exists():
                sys.stdout.write("==============================================\n")
                sys.stdout.write("WARNING: linod (worker process) is not runner.\n")
                sys.stdout.write("==============================================\n")
            from lino.modlib.linod.tasks import Tasks
            status = Tasks().status()
            if not (count := len(status)):
                sys.stdout.write(f"found 0 system tasks.\n")
                return
            sys.stdout.write(f"found {count} system tasks.\n")
            for s in status:
                sys.stdout.write(f"{s}\n")
            return

        if not (settings.SITE.site_dir / 'log_sock').exists():
            sys.stdout.write("Linod (worker process) is not runner.\n")
            return

        sockd = str(settings.SITE.site_dir / 'sockd')
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            try:
                os.unlink(sockd)
            except OSError:
                pass
            sock.bind(sockd)
            async_to_sync(get_channel_layer().send)(LINOD, {'type': 'job.list'})
            sock.listen(1)
            client_sock, _ = sock.accept()
            data = pickle.loads(get_from_socket(client_sock))
            client_sock.close()
            if len(data):
                sys.stdout.write(f"found {len(data)} system tasks:\n")
                for item in data:
                    sys.stdout.write(f"{item}\n")
            else:
                sys.stdout.write(f"found 0 system tasks.\n")
        os.remove(sockd)
