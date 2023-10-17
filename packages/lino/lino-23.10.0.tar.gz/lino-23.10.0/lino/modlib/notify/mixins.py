# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import multiprocessing as mp
# import pickle
from etgen.html import E, tostring
from asgiref.sync import async_to_sync
from django.conf import settings
# from channels.layers import get_channel_layer
from lino.api import dd, rt, _

PUBLIC_GROUP = 'all_users_channel'
# CHANNEL_LAYER = get_channel_layer()

class ChangeNotifier(dd.Model):

    class Meta(object):
        abstract = True

    if dd.is_installed('notify'):

        def get_change_subject(self, ar, cw):
            ctx = dict(user=ar.user, what=str(self))
            if cw is None:
                return _("{user} created {what}").format(**ctx)
                # msg = _("has been created by {user}").format(**ctx)
                # return "{} {}".format(self, msg)
            if len(list(cw.get_updates())) == 0:
                return
            return _("{user} modified {what}").format(**ctx)
            # msg = _("has been modified by {user}").format(**ctx)
            # return "{} {}".format(self, msg)

        def add_change_watcher(self, user):
            pass
            # raise NotImplementedError()

        def get_change_body(self, ar, cw):
            ctx = dict(user=ar.user, what=ar.obj2htmls(self))
            if cw is None:
                html = _("{user} created {what}").format(**ctx)
                html = "<p>{}</p>.".format(html)
            else:
                items = list(cw.get_updates_html(["_user_cache"]))
                if len(items) == 0:
                    return
                html = _("{user} modified {what}").format(**ctx)
                html = "<p>{}:</p>".format(html)
                html += tostring(E.ul(*items))
            return "<div>{}</div>".format(html)

        # def get_change_info(self, ar, cw):
        #     return []

        def get_change_owner(self):
            return self

        def get_change_observers(self, ar=None):
            """
            Return or yield a list of `(user, mail_mode)` tuples who are
            observing changes on this object.  Returning an empty list
            means that nobody gets notified.

            Subclasses may override this. The default implementation
            forwards the question to the owner if the owner is
            ChangeNotifier and otherwise returns an empty list.
            """
            owner = self.get_change_owner()
            if owner is self:
                return []
            if not isinstance(owner, ChangeNotifier):
                return []
            return owner.get_change_observers(ar)

        def get_notify_message_type(self):
            return rt.models.notify.MessageTypes.change

        def after_ui_save(self, ar, cw):
            # Emits notification about the change to every observer.
            super().after_ui_save(ar, cw)
            if not dd.is_installed('notify'):
                # happens e.g. in amici where we use calendar without notify
                return
            mt = self.get_notify_message_type()
            if mt is None:
                return
            def msg(user, mm):
                subject = self.get_change_subject(ar, cw)
                if not subject:
                    return None
                permalink_uris = ar.permalink_uris
                ar.permalink_uris = True
                body = self.get_change_body(ar, cw)
                ar.permalink_uris = permalink_uris
                return (subject, body)
            owner = self.get_change_owner()
            # if settings.SITE.use_multiprocessing:
            #     proc = mp.Process(
            #         target=rt.models.notify.Message.emit_notification,
            #         args=(ar, owner, mt, msg, self.get_change_observers(ar)))
            #     proc.start()
            # else:
            rt.models.notify.Message.emit_notification(
                ar, owner, mt, msg, self.get_change_observers(ar))
