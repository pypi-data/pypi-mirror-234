# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

from django.conf import settings

from typing import Callable
from django.utils.timezone import now
from lino.api import dd, _

class Procedure(dd.Choice):
    func: Callable
    every_unit: str
    every_value: int
    # start_datetime = now()

    def run(self, ar):
        self.func(ar)

    def __repr__(self):
        return f"Procedures.{self.value} every {self.every_value} {self.every_unit}"


class Procedures(dd.ChoiceList):
    verbose_name = _("Background procedure")
    verbose_name_plural = _("Background procedures")
    max_length = 100
    item_class = Procedure
    column_names = "value name text every_unit every_value"

    @dd.virtualfield(dd.CharField(_("Recurrency")))
    def every_unit(cls, choice, ar):
        return choice.every_unit

    @dd.virtualfield(dd.CharField(_("Repeat every")))
    def every_value(cls, choice, ar):
        return choice.every_value


# class LogLevels(dd.ChoiceList):
#     pass
#
# add = LogLevels.add_item
# add('DEBUG', "DEBUG", 'debug')
# add('INFO', "INFO", 'info')
# add('WARNING', "WARNING", 'warning')
# add('ERROR', "ERROR", 'error')
# add('CRITICAL', "CRITICAL", 'critical')
