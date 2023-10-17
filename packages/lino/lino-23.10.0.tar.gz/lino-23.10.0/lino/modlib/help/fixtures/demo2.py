# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.conf import settings
from lino.api import dd, rt, _
from lino.api.shell import help, contacts

if dd.get_plugin_setting("help", "use_contacts"):

    def site_contact(type, company=None, **kwargs):
        return help.SiteContact(site_contact_type=type, company=company, **kwargs)


    def objects():
        yield site_contact("owner", settings.SITE.site_config.site_company)
        yield site_contact("maintainer", contacts.Company.objects.get(pk=106))
        yield site_contact("hotline",
            contact_person=contacts.Person.objects.get(pk=113),
            **dd.babelkw('remark', _("Mon and Fri from 11:30 to 12:00")))
