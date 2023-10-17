# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from importlib.util import find_spec
has_channels = find_spec('channels') is not None
import sys
import logging
import traceback
from logging.handlers import SocketHandler


class LinoSocketHandler(SocketHandler):
    # see: https://code.djangoproject.com/ticket/29186
    def emit(self, record):
        if hasattr(record, 'request'):
            record.request = "Removed by LinoSocketHandler"
        try:
            return super().emit(record)
        except Exception as e:
            logging.warning(f"Non-picklable LogRecord: {record}\n" + dd.read_exception(sys.exc_info()))

if has_channels:
    
    from django.conf import settings

    class LinodFilter(logging.Filter):
        def filter(self, record):
            # if record.name.split('.')[0] in settings.SITE.auto_configure_logger_names:
            #     return 0
            return 1

else:

    class LinodFilter(logging.Filter):
        def filter(self, record):
            return 1
