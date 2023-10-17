# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings

LINOD = "linod_" + settings.SITE.site_dir.name

log_sock_path = settings.SITE.site_dir / 'log_sock'
worker_sock_path = settings.SITE.site_dir / 'worker_sock'
