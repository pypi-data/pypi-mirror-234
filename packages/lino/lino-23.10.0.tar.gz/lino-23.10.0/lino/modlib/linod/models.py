# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
import sys
import traceback
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async


from lino.api import dd, rt, _

from lino.core.roles import SiteStaff
from lino.mixins import Sequenced

from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.system.mixins import RecurrenceSet
from .choicelists import Procedures, Procedure

# logger = logging.getLogger(__name__)


# class SetupTasks(dd.Action):
#     """Run this only in development environment."""
#     label = _("Setup tasks")
#     help_text = _("Run this action only in development environment (not designed for production environment).")
#     select_rows = False
#
#     def run_from_ui(self, ar, **kwargs):
#         if not settings.SITE.is_demo_site:
#             ar.error(message="Action is not allowed in production site.")
#             return
#         from lino.modlib.linod.tasks import Tasks
#         Tasks().setup()
#         ar.success(refresh_all=True)


class RunNow(dd.Action):
    label = _("Run job")
    select_rows = True

    def run_from_ui(self, ar, **kwargs):
        for rule in ar.selected_rows:
            assert isinstance(rule, rt.models.linod.JobRule)
            rule.start_job(ar)
        ar.set_response(refresh_all=True)


class JobRule(Sequenced, RecurrenceSet):
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'JobRule')
        app_label = 'linod'
        verbose_name = _("Job rule")
        verbose_name_plural = _("Job rules")

    # name = dd.CharField(max_length=50, default="", blank=True)
    procedure = Procedures.field(strict=False, unique=True)
    # log_level = LogLevels.field(default='debug')
    disabled = dd.BooleanField(default=False)
    silent = dd.BooleanField(default=True)

    # setup_tasks = SetupTasks()
    run_now = RunNow()

    def disabled_fields(self, ar):
        df = super().disabled_fields(ar)
        df.add('procedure')
        return df

    @classmethod
    async def run_them_all(cls, ar):
        # dd.logger.info("20231010 run_them_all()")
        now = timezone.now()
        next_time = now + timedelta(seconds=12)
        rules = await sync_to_async(cls.objects.filter)(disabled=False)
        # rules = cls.objects.filter(disabled=False)
        async for jr in rules:
        # for jr in rules:
            # dd.logger.info("20231010 start %s", jr)
            nsd = jr.get_next_suggested_date(ar, now)
            if nsd <= now:
                job = jr.start_job(ar)
                # done.append(job)
                nsd = jr.get_next_suggested_date(ar, job.end_time)
            next_time = min(next_time, nsd)

        # dd.logger.info("20231010 run_them_all() returns %s", next_time)
        return next_time

    def start_job(self, ar):
        Job = rt.models.linod.Job
        job, created = Job.objects.get_or_create(rule=self)
        if job.end_time is None and not created:
            raise Warning("There is already a job running for {}".format(self))
            # return
        if not self.silent:
            dd.logger.info("Start background job %s", self)
        job.start_time = timezone.now()
        job.end_time = None
        job.message = ''
        job.full_clean()
        job.save()

        try:
            self.procedure.run(ar)
            job.message = ar.response.get('info_message', '')
        except Exception as e:
            self.disabled = True
            job.message = ''.join(traceback.format_exception(e))
            job.end_time = timezone.now()
        job.full_clean()
        job.save()
        # Job.objects.exclude(
        #     pk__in=list(Job.objects.filter(
        #         rule=self
        #     ).order_by("-start_datetime").values_list('pk', flat=True)[:dd.plugins.linod.remove_after])
        # ).filter(rule=self).delete()
        return job

    def __str__(self):
        r = f"Job rule #{self.pk} {self.procedure.value}"
        if self.disabled:
            r += " ('disabled')"
        return r

    # def __repr__(self):
    #     r = f"Job rule #{self.pk} <{self.procedure!r}>"
    #     if self.disabled:
    #         r += " ('disabled')"
    #     return r


class Job(dd.Model):
    allow_cascaded_delete = ['rule']

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Job')
        app_label = 'linod'
        verbose_name = _("Background job")
        verbose_name_plural = _("Background jobs")
        ordering = ['-start_time']

    start_time = dd.DateTimeField(null=True, editable=False)
    end_time = dd.DateTimeField(null=True, editable=False)
    # rule = dd.ForeignKey('linod.JobRule', null=False, blank=False, editable=False, unique=True)
    rule = dd.OneToOneField('linod.JobRule', null=False, blank=False, editable=False)
    message = dd.TextField(editable=False)

    def __str__(self):
        r = f"Job {self.rule}"
        return r


class Jobs(dd.Table):
    model = 'linod.Job'
    required_roles = dd.login_required(SiteStaff)
    column_names = "start_time end_time rule message *"
    detail_layout = """
    rule
    start_time end_time
    message
    """


class JobsByRule(Jobs):
    master_key = 'rule'
    column_names = "start_time end_time message *"


class JobRules(dd.Table):
    # label = _("System tasks")
    model = 'linod.JobRule'
    required_roles = dd.login_required(SiteStaff)
    column_names = "seqno procedure every every_unit silent disabled *"
    detail_layout = """
    seqno procedure every every_unit
    silent disabled
    linod.JobsByRule
    """
    insert_layout = """
    procedure
    every every_unit
    """


class JobsChecker(Checker):
    """Checks for the following repairable problem:

    - :message:`Must update phonetic words.`

    """
    verbose_name = _("Check for missing job rules")
    model = None

    def get_checkdata_problems(self, obj, fix=False):
        JobRule = rt.models.linod.JobRule

        for proc in Procedures.get_list_items():
            # dd.logger.info(f"Create job rule from {proc!r}")
            qs = JobRule.objects.filter(procedure=proc)
            if qs.count() == 0:
                msg = _("Missing job rule for {}").format(proc)
                yield (True, msg)
                if fix:
                    jr = JobRule(procedure=proc,
                        every_unit=proc.every_unit, every=proc.every_value)
                    jr.full_clean()
                    jr.save()

JobsChecker.activate()
