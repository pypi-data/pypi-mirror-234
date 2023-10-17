# -*- coding: UTF-8 -*-
# Copyright 2020-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import logging; logger = logging.getLogger(__name__)
import json
from django.conf import settings
from django.utils.timezone import now
from lino.api import rt, dd
from lino.modlib.linod.utils import LINOD

NOTIFICATION = "NOTIFICATION"
CHAT = "CHAT"

NOTIFICATION_TYPES = [
    NOTIFICATION, CHAT
]


def send_notification(user=None, primary_key=None, subject=None, body=None,
    created=None, action_url=None, action_title="OK"):
    """

    `action_url` : the URL to show when user clicks on the
    OK button of their desktop notification.

    """
    if user is None:
        return

    created = created.strftime("%a %d %b %Y %H:%M")

    if settings.SITE.use_linod:
        # importing channels at module level would cause certain things to fail
        # when channels isn't installed, e.g. `manage.py prep` in `lino_book.projects.workflows`.
        from channels.layers import get_channel_layer
        from channels.exceptions import ChannelFull
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()

        msg = dict(
            type=NOTIFICATION,
            subject=subject,
            id=primary_key,
            body=body,
            created=created,
            action_url=action_url
        )

        try:
            async_to_sync(channel_layer.group_send)(str(user.id),
                                                    {"type": "send.notification",  # method name in consumer
                                                     "text": json.dumps(msg)})  # data
        except Exception as E:
            logger.exception(E)

        if dd.plugins.notify.use_push_api:
            data = dict(action_url=action_url, subject=subject, body=body, action_title=action_title)
            try:
                async_to_sync(channel_layer.send)(LINOD, {
                    'type': 'send.push',
                    'data': data,
                    'user_id': user.id if user is not None else None
                })
            except ChannelFull as e:  # happens on older Pythons and can cause many tracebacks
                # logger.exception(e)
                # logger.warning(str(e))
                pass
