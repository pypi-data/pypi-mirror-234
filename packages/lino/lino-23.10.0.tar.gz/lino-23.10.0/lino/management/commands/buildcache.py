# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        # print("20231005", verbosity)
        settings.SITE.build_site_cache(force=True, verbosity=verbosity)
