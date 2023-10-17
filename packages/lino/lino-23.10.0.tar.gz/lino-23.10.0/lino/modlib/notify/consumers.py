# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import json
import logging
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class ClientConsumer(AsyncWebsocketConsumer):
    groups = []
    user = None

    async def connect(self):
        await self.accept()
        if not self.channel_name:
            # 20230216 on Jane we had TypeError: int() argument must be a
            # string, a bytes-like object or a number, not 'NoneType'
            return
        self.user = self.scope.get('user')
        await self.channel_layer.group_add('broadcast', self.channel_name)
        if not self.user.is_anonymous:
            await self.channel_layer.group_add(str(self.user.id), self.channel_name)

        # await self.chat_connect()

    async def send_notification(self, text):
        await self.send(text_data=text['text'])

    # async def receive(self, text_data: str = None, bytes_data: bytes = None):
    #
    #     await self.chat_receive(text_data, bytes_data)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('broadcast', self.channel_name)
        if not self.user.is_anonymous:
            await self.channel_layer.group_discard(str(self.user.id), self.channel_name)

        # await self.chat_disconnect(close_code)

    # async def chat_connect(self):
    #     if settings.SITE.is_installed('chat') and self.user.is_authenticated:
    #         try:
    #             ChatGroupMember = settings.SITE.models.chat.ChatGroupMember
    #             self.groups = await database_sync_to_async(lambda: [
    #                 'chat_group_' + str(item[0]) for item in \
    #                 ChatGroupMember.objects.select_related('group').filter(user=self.user).values_list('group_id')
    #             ])()
    #             for group_name in self.groups:
    #                 await self.channel_layer.group_add(group_name, self.channel_name)
    #         except Exception as e:
    #             logger.exception(e)
    #
    # async def chat_receive(self, text_data: str = None, bytes_data: bytes = None):
    #     if settings.SITE.is_installed('chat') and self.user.is_authenticated:
    #         try:
    #             data = json.loads(text_data)
    #
    #             data["user"] = self.user
    #             if settings.SITE.is_installed("chat"):
    #                 ChatMessage = settings.SITE.models.chat.ChatMessage
    #                 function = data.get('function', None)
    #                 if function is not None and hasattr(ChatMessage, function):
    #                     data = await database_sync_to_async(getattr(ChatMessage, function))(data)
    #                     if data is not None:
    #                         await self.channel_layer.group_send('chat_group_' + str(data[6]), {
    #                             'type': 'chatter',
    #                             'data': data
    #                         })
    #         except Exception as E:
    #             logger.exception(E)
    #             raise E

    # async def chatter(self, event):
    #     data = event['data']
    #     seen = await database_sync_to_async(
    #         settings.SITE.models.chat.ChatSeen.objects.filter(chat=data[4], user=self.user).first
    #     )()
    #     if seen:
    #         data[3] = json.loads(json.dumps(seen.created, cls=DjangoJSONEncoder))
    #     await self.send(text_data=json.dumps({
    #         'type': 'CHAT',
    #         'chat': data
    #     }))

    # async def chat_disconnect(self, close_code: int = None):
    #     if settings.SITE.is_installed('chat'):
    #         for group_name in self.groups:
    #             await self.channel_layer.group_discard(group_name, self.channel_name)
