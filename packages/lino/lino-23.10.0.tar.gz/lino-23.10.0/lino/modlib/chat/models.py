# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils.format_date import fds
from lino.modlib.office.roles import OfficeUser
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.memo.mixins import Previewable
from lino.mixins import Created, ObservedDateRange, BabelNamed, Referrable
# from lino_noi.lib.groups.models import Group
from lino.core.site import html2text
from lino.core.requests import BaseRequest
from lino.core.gfks import gfk2lookup
from lino.api import dd, rt, _
from lino import DJANGO2
from etgen.html import E, tostring
from django.utils import translation
from django.utils import timezone
from django.conf import settings
from django.db import models
from datetime import timedelta
from datetime import datetime
from lxml import etree
from io import StringIO
import json
import logging

from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)

html_parser = etree.HTMLParser()


def groupname(s):
    # Remove any invalid characters from the given string so that it can
    # be used as a Redis group name.
    # "Group name must be a valid unicode string containing only
    # alphanumerics, hyphens, or periods."

    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')


class ChatGroup(UserAuthored, Created, Referrable):
    class Meta(object):
        app_label = 'chat'
        verbose_name = _("Chat group")
        verbose_name_plural = _("Chat groups")
        ordering = ['created', 'id']

    title = dd.CharField(max_length=20)
    description = dd.RichTextField(max_length=200, blank=True, null=True);
    ticket = dd.ForeignKey("tickets.Ticket", blank=True, null=True);

    @dd.action(_("getChatGroups"))
    def getChatGroups(self, ar):
        """
        Returns info on all GroupChats for this user.
        """
        qs = ChatGroupMember.objects.filter(user=ar.get_user()).select_related("group")

        rows = [{"id": cgm.group.pk,
                 "title": cgm.group.title,
                 "unseen": cgm.group.get_unseen_count(ar)} for cgm in qs]

        return ar.success(rows=rows)

    def get_unseen_count(self, ar):
        """
        Returns count of messages that haven't been seen yet."""
        return rt.models.chat.ChatMessage.objects.filter(group=self).annotate(seen=models.Case(
            models.When(models.Exists(rt.models.chat.ChatSeen.objects.filter(
                chat__pk=models.OuterRef('pk'),
                user=ar.get_user()
            )), then=models.Value(True)),
            output_field=models.BooleanField(),
            default=models.Value(False)
        )).filter(seen=False).count()

    @dd.action(_("Load GroupChat"))
    def loadGroupChat(self, ar):
        """Returns chat messages for a given chat"""
        rows = []
        if 'mk' in ar.rqdata:
            # master = rt.models.resolve("contenttypes.ContentType").get(pk=ar.rqdata['mt']).get(pk=ar.rqdata["mk"])
            ar.selected_rows = [ChatGroup.objects.get(ticket__pk=ar.rqdata['mk'])]
        for group in ar.selected_rows:
            last_ten = rt.models.chat.ChatMessage.objects.filter(group=group).order_by('-sent')[:10]
            rows.append({
                'title': group.title,
                'id': group.id,
                'messages': [cm.serialize(ar) for cm in last_ten]
            })
        return ar.success(rows=rows)


class ChatGroupMember(Created):
    class Meta(object):
        app_label = 'chat'

    user = dd.ForeignKey(
        'users.User',
        verbose_name=_("Author"),
        related_name="ChatGroups",
        blank=True, null=True)

    group = dd.ForeignKey(ChatGroup, related_name="ChatGroupsMembers")


class ChatMessage(UserAuthored, Created, Previewable):
    class Meta(object):
        app_label = 'chat'
        verbose_name = _("Chat message")
        verbose_name_plural = _("Chat messages")
        ordering = ['created', 'id']

    # message_type = MessageTypes.field(default="change")

    sent = models.DateTimeField(_("sent"), auto_now_add=True, editable=False)
    group = dd.ForeignKey(
        'chat.ChatGroup', blank=True, null=True, verbose_name=_('Group'), related_name="messages")
    hash = dd.CharField(_("Hash"), max_length=25, null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.user, self.body)

    def serialize(self, ar=None):
        if ar is None:
            ar = BaseRequest()
        return [
            self.user.username,
            ar.parse_memo(self.body),
            json.loads(json.dumps(self.sent, cls=DjangoJSONEncoder)),
            None,
            self.pk,
            self.user.id,
            self.group.id,
            self.hash,
            self.group.ticket.id if self.group.ticket else None,
        ]

    @classmethod
    def markAsSeen(cls, data):
        group_id = data['body'][0]
        # mark all as seen, don't bother for the truth for now
        ChatSeen = rt.models.chat.ChatSeen
        last = ChatSeen.objects.select_related('chat').filter(chat__group__id=group_id, user=data['user']).first()
        filter = dict(group=group_id)
        if last is not None:
            filter.update(sent__gt=last.chat.sent)
        ChatSeen.objects.bulk_create(
            [ChatSeen(chat=chat, user=data['user'], created=timezone.now()) for chat in cls.objects.filter(**filter)])


    @classmethod
    def onRecive(cls, data):
        args = dict(
            user=data['user'],
            body=data['body']['body'],
            group_id=data['body']['group_id'],
            hash=data['body']['hash']
        )
        newMsg = cls(**args)
        newMsg.full_clean()
        newMsg.save()
        return newMsg.serialize()


class ChatSeen(UserAuthored, Created):
    class Meta(object):
        app_label = 'chat'
        # verbose_name = _("Chat message")
        # verbose_name_plural = _("Chat messages")
        ordering = ['-created']

    chat = dd.ForeignKey(ChatMessage, related_name="chatSeen")


from .ui import *
