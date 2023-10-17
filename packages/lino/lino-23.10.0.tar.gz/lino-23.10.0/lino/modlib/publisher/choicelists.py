# -*- coding: UTF-8 -*-
# Copyright 2020-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


import os
from copy import copy

from django.db import models
from django.conf import settings
from django.utils import translation
from django.utils.text import format_lazy

from lino.api import dd, _
from lino.mixins.registrable import RegistrableState

from lino.modlib.jinja.choicelists import JinjaBuildMethod
from lino.modlib.printing.choicelists import BuildMethods

class PublisherBuildMethod(JinjaBuildMethod):

    template_ext = '.pub.html'
    templates_name = 'pub'
    default_template = 'default.pub.html'
    target_ext = '.html'
    name = 'pub'

    def build(self, ar, action, elem):
        filename = action.before_build(self, elem)
        if filename is None:
            return
        tpl = self.get_template(action, elem)
        lang = str(elem.get_print_language()
                   or settings.SITE.DEFAULT_LANGUAGE.django_code)
        ar = copy(ar)
        ar.renderer = settings.SITE.plugins.jinja.renderer
        # ar.tableattrs = dict()
        # ar.cellattrs = dict(bgcolor="blue")

        with translation.override(lang):
            cmd_options = elem.get_build_options(self)
            dd.logger.info(
                "%s render %s -> %s (%r, %s)",
                self.name, tpl.lino_template_names, filename, lang, cmd_options)
            context = elem.get_printable_context(ar)
            html = tpl.render(context)
            self.html2file(html, filename)
            return os.path.getmtime(filename)

    def html2file(self, html, filename):
        raise NotImplementedError()


BuildMethods.add_item_instance(PublisherBuildMethod())



class PublishingState(RegistrableState):
    is_published = False


class PublishingStates(dd.Workflow):
    item_class = PublishingState
    verbose_name = _("Publishable state")
    verbose_name_plural = _("Publishable states")
    column_names = "value name text is_published"

    @classmethod
    def get_published_states(cls):
        return [o for o in cls.objects() if o.is_published]

    @dd.virtualfield(models.BooleanField(_("published")))
    def is_published(cls, choice, ar):
        return choice.is_published

add = PublishingStates.add_item
add('10', _("Draft"), 'draft')
add('20', _("Published"), 'published', is_published=True)
add('30', _("Removed"), 'removed')


class PublisherView(dd.Choice):
    table_class = None  # TODO: rename this to data_view

    def __init__(self, location, table_class, text=None):
        self.table_class = table_class
        self.publisher_location = location
        # model = dd.resolve_model(table_class.model)
        # self.model = model
        # value = dd.full_model_name(model)
        value = str(table_class)
        if text is None:
            text = format_lazy("{} ({})", location, table_class)
            # text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
            # text = model._meta.verbose_name + ' (%s.%s)' % (
            # text = format_lazy("{} ({})", model._meta.verbose_name, value)
        #     model.__module__, model.__name__)
        name = None
        super().__init__(value, text, name)


class PublisherViews(dd.ChoiceList):
    item_class = PublisherView
    verbose_name = _("Publisher view")
    verbose_name_plural = _("Publisher views")
    column_names = "location value name text data_view *"

    @dd.virtualfield(models.CharField(_("Location")))
    def location(cls, choice, ar):
        return choice.publisher_location

    @dd.virtualfield(models.CharField(_("Data view")))
    def data_view(cls, choice, ar):
        return choice.table_class
