# Copyright 2010-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""See :doc:`/specs/uploads`.


"""
from os.path import join
from lino import ad, _
from lino.modlib.memo.parser import split_name_rest


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Uploads")
    menu_group = "office"

    remove_orphaned_files = False
    """
    Whether `checkdata --fix` should automatically delete orphaned files in the
    uploads folder.

    """

    def on_ui_init(self, kernel):
        # from django.conf import settings
        super().on_ui_init(kernel)
        self.site.makedirs_if_missing(self.get_uploads_root())

    def get_uploads_root(self):
        # from django.conf import settings
        # return join(settings.SITE.MEDIA_ROOT, 'uploads')
        return join(self.site.django_settings['MEDIA_ROOT'], 'uploads')

    def setup_main_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.MyUploads')

    def setup_config_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.Volumes')
        m.add_action('uploads.UploadTypes')

    def setup_explorer_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.AllUploads')
        m.add_action('uploads.UploadAreas')

    def post_site_startup(self, site):

        # def photorow(ar, text, cmdname, mentions):
        #     Upload = site.models.uploads.Upload
        #     photos = [Upload.objects.get(pk=int(pk)) for pk in text.split()]
        #     # ctx = dict(width="{}%".format(int(100/len(photos))))
        #     return ''.join([obj.memo2html(ar, obj.description) for obj in photos])
        #
        # site.plugins.memo.parser.register_command('photorow', photorow)

        if site.is_installed("memo"):

            def gallery(ar, text, cmdname, mentions):
                Upload = site.models.uploads.Upload
                photos = [Upload.objects.get(pk=int(pk)) for pk in text.split()]
                # ctx = dict(width="{}%".format(int(100/len(photos))))
                mentions.update(photos)
                html = ''.join([obj.memo2html(ar, obj.description) for obj in photos])
                return "<p align=\"center\">{}</p>".format(html)

            site.plugins.memo.parser.register_command('gallery', gallery)

        super().post_site_startup(site)
