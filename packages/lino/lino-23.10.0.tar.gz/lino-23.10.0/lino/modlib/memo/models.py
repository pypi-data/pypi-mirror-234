# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from PIL.Image import open as imgopen
from typing import overload
from django.contrib.contenttypes.models import ContentType
from django.utils.text import format_lazy
# from rstgen.sphinxconf.sigal_image import line2html
from lino.api import dd, rt, _
from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.gfks.fields import GenericForeignKey, GenericForeignKeyIdField
from .parser import split_name_rest
# from .mixins import *


# Translators: will also be concatenated with '(type)' '(object)'
source_label = _("Source")

class Mention(Controllable):

    class Meta(object):
        app_label = 'memo'
        abstract = dd.is_abstract_model(__name__, 'Mention')
        verbose_name = _("Mention")
        verbose_name_plural = _("Mentions")

    source_type = dd.ForeignKey(
        ContentType,
        editable=True,
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_source_set",
        verbose_name=format_lazy("{} {}", source_label, _('(type)')))

    source_id = GenericForeignKeyIdField(
        source_type,
        editable=True,
        blank=True, null=True,
        verbose_name=format_lazy("{} {}", source_label, _('(object)')))

    source = GenericForeignKey(
        'source_type', 'source_id',
        verbose_name=source_label)


class Mentions(dd.Table):
    required_roles = dd.login_required(SiteStaff)
    editable = False
    model = "memo.Mention"
    column_names = "source owner *"
    # detail_layout = """
    # id comment owner created
    # """

class MentionsByOwner(Mentions):
    master_key = "owner"
    column_names = "source *"
