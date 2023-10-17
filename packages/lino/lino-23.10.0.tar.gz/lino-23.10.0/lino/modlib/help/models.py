# Copyright 2021-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.utils.translation import get_language
from lino.core.actors import Actor
from lino.api import dd, _
from lino.modlib.memo.mixins import MemoReferrable
from lino_xl.lib.contacts.mixins import ContactRelated

use_contacts = dd.get_plugin_setting('help', 'use_contacts')
make_help_pages = dd.get_plugin_setting('help', 'make_help_pages')

class OpenHelpWindow(dd.Action):

    action_name = 'open_help'
    # icon_name = 'help'
    default_format = 'ajax'
    button_text = '?'
    select_rows = False
    help_text = _('Open Help Window')
    show_in_plain = True

    # def js_handler(self, actor):
    #     parts = ['cache', 'help']
    #     if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
    #         parts.append(get_language())
    #     parts.append(str(actor) + ".html")
    #     url = settings.SITE.build_site_cache_url(*parts)
    #     # return "let _ = window.open('%s');" % url
    #     # return "() => window.open('%s')" % url
    #     return "function (){window.open('%s')}" % url
    #     # return "window.open('%s')" % url

    def run_from_ui(self, ar, **kwargs):
        # print("20210612")
        parts = ['cache', 'help']
        if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
            parts.append(get_language())
        parts.append(str(ar.actor) + ".html")
        # parts.append("index.html")
        url = settings.SITE.build_site_cache_url(*parts)
        ar.set_response(success=True)
        ar.success(open_url=url)

    # def get_a_href_target(self):
    #     parts = ['cache', 'help']
    #     if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
    #         parts.append(get_language())
    #     parts.append("index.html")
    #     return settings.SITE.build_media_url(*parts)


if make_help_pages:
    
    Actor.open_help = OpenHelpWindow()

if use_contacts:

    class SiteContactTypes(dd.ChoiceList):
        verbose_name = _("Site contact type")
        verbose_name_plural = _("Site contact types")
        # item_class = SiteContactType

    add = SiteContactTypes.add_item
    add("100", _("Site owner"), "owner")
    add("200", _("Site maintainer"), "maintainer")
    add("300", _("Hotline"), "hotline")


    class SiteContact(ContactRelated, MemoReferrable):

        class Meta:
            app_label = 'help'
            verbose_name = _("Site contact")
            verbose_name_plural = _("Site contacts")
            abstract = dd.is_abstract_model(__name__, 'SiteContact')

        order_by = ['site_contact_type', 'company', 'person']
        memo_command = 'sitecontact'

        site_contact_type = SiteContactTypes.field()
        remark = dd.BabelTextField(_('Remark'), blank=True)


    class SiteContacts(dd.Table):
        model = "help.SiteContact"
        column_names = "site_contact_type company contact_person remark"

        detail_layout = """
        site_contact_type
        company
        contact_person
        remark
        """

        insert_layout = """
        site_contact_type
        company
        contact_person
        """
