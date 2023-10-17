# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Defines the procedure for managing system (background) tasks."""

import logging
import sys
import traceback
from django.utils import timezone

from lino.api import rt

# logger = logging.getLogger('linod')


# class Tasks:
#
#     def __init__(self):
#         self.Job = rt.models.linod.Job
#         self.JobRule = rt.models.linod.JobRule
#         self.Procedures = rt.models.linod.Procedures
#
#     def status(self):
#         ar = self.JobRule.get_default_table().request()
#         return [
#             f"{rule!r}{f' next run at: {rule.get_next_suggested_date(ar, (rule.job_set.first() or rule.procedure).start_datetime)}' if not rule.disabled else ''}"
#             for rule in self.JobRule.objects.all()]
#
#     def create_rule(self, procedure):
#         logger.info(f"creating job rule for: {procedure!r}")
#         rule = self.JobRule(procedure=procedure, every_unit=procedure.every_unit, every=procedure.every_value)
#         ar = self.JobRule.get_default_table().request()
#         rule.full_clean()
#         rule.save_new_instance(ar)
#         logger.info(f"rule created: {rule!r}")
#
#     def cancel_rule(self, rule):
#         logger.warning(f"disabling rule: {rule!r}")
#         rule.disabled = True
#         rule.full_clean()
#         rule.save()
#
#     # def setup(self):
#     #     nl = '\n'
#     #     choices_values = [choice.value for choice, _ in self.Procedures.choices]
#     #
#     #     deletables = self.JobRule.objects.exclude(procedure__in=choices_values)
#     #     if deletables.exists():
#     #         logger.warning(
#     #             f"deleting rules for non-existant procedure:\n{nl.join([rule.procedure.value for rule in deletables])}")
#     #         deletables.delete()
#     #
#     #     reactivatables = self.JobRule.objects.filter(disabled=True)
#     #     if reactivatables.exists():
#     #         logger.info(f"reactivating all previously disabled rules.")
#     #         reactivatables.update(disabled=False)
#     #         logger.info(f"rules reactivated:\n{nl.join([repr(job) for job in reactivatables])}")
#     #
#     #     for choice, _ in self.Procedures.choices:
#     #         if not self.JobRule.objects.filter(procedure=choice).exists():
#     #             self.create_rule(choice)
#
#     def run(self):
#         ar = self.JobRule.get_default_table().request()
#         rules = self.JobRule.objects.filter(disabled=False)
#         doables = []
#         now = timezone.now()
#         dates = []
#         for rule in rules:
#             n = rule.get_next_suggested_date(ar, (rule.job_set.first() or rule.procedure).start_datetime)
#             if n <= now:
#                 doables.append(rule)
#             else:
#                 dates.append(n)
#         for rule in doables:
#             job = rule.run(ar, logger)
#             dates.append(rule.get_next_suggested_date(ar, job.start_datetime))
#
#         if not dates:
#             if doables:
#                 return True
#             return False
#
#         return min(dates)
