# -*- coding: UTF-8 -*-
# Copyright 2013-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from pathlib import Path
from django.core.management import call_command
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from rstgen.utils import confirm
from lino.management.commands.initdb import Command as BaseCommand
from lino.management.commands.initdb import CommandError


class Command(BaseCommand):
    help = "Flush the database and load the default demo fixtures."

    def handle(self, *args, **options):
        fixtures = options.get('fixtures', args)
        if len(fixtures) > 0:
            raise CommandError(
                "This command takes no arguments (got %r)" % fixtures)

        if settings.SITE.readonly:
            settings.SITE.logger.info(
                "No need to `prep` readonly site '%s'.",
                settings.SETTINGS_MODULE)
            return

        if settings.SITE.master_site:
            settings.SITE.logger.info(
                "No need to `prep` slave site '%s'.", settings.SETTINGS_MODULE)
            return

        args = settings.SITE.demo_fixtures
        if isinstance(args, str):
            args = args.split()
        options['fixtures'] = args

        if settings.SITE.is_installed('search') and settings.SITE.use_elasticsearch:
            call_command('createindexes', '-i')

        options.update(remove_media=True)
        super().handle(**options)

        settings.SITE.kernel.mark_virgin()
