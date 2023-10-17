# -*- coding: UTF-8 -*-
# Copyright 2020-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django import http
from django.views.generic import View

from lino.core import auth
from lino.core.requests import BaseRequest, ActionRequest

from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie


class Element(View):

    # actor = None
    publisher_view = None

    def get(self, request, pk=None):
        # print("20220927 a get()")
        if pk is None:
            return http.HttpResponseNotFound()
        # rnd = settings.SITE.kernel.default_renderer
        rnd = settings.SITE.plugins.publisher.renderer

        # kw = dict(actor=self.publisher_model.get_default_table(),
        #     request=request, renderer=rnd, permalink_uris=True)
        kw = dict(renderer=rnd)
        # kw = dict(renderer=rnd, permalink_uris=True)
        # if rnd.front_end.media_name == 'react':
        #     kw.update(hash_router=True)

        kw.update(selected_pks=[pk])

        ar = self.publisher_view.table_class.request(request=request, **kw)
        # ar = self.actor.request(request=request, **kw)
        # obj = ar.get_row_by_pk(pk)
        # if obj is None:
        #     return http.HttpResponseNotFound()
        # return obj.get_publisher_response(ar)
        return ar.selected_rows[0].get_publisher_response(ar)

class Index(View):

    def get(self, request, pk=1):
        rnd = settings.SITE.plugins.publisher.renderer
        dv = settings.SITE.models.pages.Nodes
        index_node = dv.model.objects.get(ref="index")
        ar = dv.request(request=request, renderer=rnd, selected_rows=[index_node])
        return index_node.get_publisher_response(ar)
