# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
# from importlib.util import find_spec
# has_channels = find_spec('channels') is not None
# if has_channels:

if settings.SITE.use_linod:
    from daphne.management.commands.runserver import Command
else:
    from django.contrib.staticfiles.management.commands.runserver import Command
