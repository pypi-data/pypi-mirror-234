# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This defines the :class:`Plugin` class.

See :doc:`/dev/plugins`.

"""

import os
import inspect
from os.path import exists, join, dirname, isdir, abspath
from collections.abc import Iterable
from urllib.parse import urlencode


class Plugin(object):
    """The base class for all plugin descriptors.
    """

    verbose_name = None
    """The verbose name of this plugin, as shown to the user.  This can be
    a lazily translated string.

    """

    short_name = None
    """The abbreviated name of this plugin, shown to the user in places
    where shortness is important, e.g. as the label of the tabs of a
    detail layout.  This can be a lazily translated string. Defaults
    to :attr:`verbose_name`.

    """

    needs_plugins = []
    """A list of names of plugins needed by this plugin.

    The default implementation of :meth:`get_required_plugins` returns this list.

    """

    needed_by = None
    """If not None, then it is the Plugin instance which caused this
    plugin to automatically install.

    """

    extends_models = None
    """If specified, a list of model names for which this app provides a
    subclass.

    For backwards compatibility this has no effect
    when :setting:`override_modlib_models` is set.

    """

    disables_plugins = []
    """A list of strings with names of plugins to **not** install even
    though they are yeld by :meth:`get_installed_apps
    <lino.core.site.Site.get_installed_apps>`. This is applied as an
    additional plugin filter even after :meth:`get_apps_modifiers
    <lino.core.site.Site.get_apps_modifiers>`.

    The plugin names can be either the full name or just the
    app_label.

    This list is allowed to contain names of plugins which are not
    installed at all.

    Usage example: The :mod:`lino.modlib.tinymce` works only with
    ExtJS 3, and we currently believe that we will never need it in
    ExtJS 6.  When switching back and forth between
    :mod:`lino.modlib.extjs` and :mod:`lino_extjs6.extjs6`, we had to
    remove it explicitly by also defining a :meth:`get_apps_modifiers
    <lino.core.site.Site.get_apps_modifiers>` method::

        def get_apps_modifiers(self, **kw):
            kw = super(Site, self).get_apps_modifiers(**kw)
            kw.update(tinymce=None)
            return kw

    Now :mod:`lino_extjs6.extjs6` has :attr:`disables_plugins` set to
    ``['tinymce']`` and we no longer need above code because Lino now
    removes it automatically when ExtJS 6 is being used.

    """

    ui_label = None

    ui_handle_attr_name = None
    """Currently implemented by :mod:`lino.modlib.extjs`,
    :mod:`lino.modlib.bootstrap3`."""

    menu_group = None
    """The name of another plugin to be used as menu group.

    See :meth:`get_menu_group`.
    """

    media_base_url = None
    """
    Remote URL base for media files.

    """

    media_name = None
    """
    Either `None` (default) or a non-empty string with the name of the
    subdirectory of your :xfile:`media` directory which is expected to
    contain media files for this app.

    `None` means that there this app has no media files of her own.

    Best practice is to set this to the `app_label`.  Will be ignored
    if :attr:`media_base_url` is nonempty.

    """

    url_prefix = None
    """
    The url prefix under which this plugin should ask to
    install its url patterns.
    """

    site_js_snippets = []
    """
    List of js snippets to be injected into the `lino_*.js` file.

    """

    support_async = False
    """Whether this plugin uses :class:`lino.core.utils.DelayedValue`."""


    renderer = None
    """The renderer used by this plugin. See :doc:`/dev/rendering`."""

    _active = True
    """Whether this plugin is active.
    """

    def __init__(self, site, app_label, app_name, app_module, needed_by, configs: dict):
        """This is called when the Site object *instantiates*, i.e.  you may
        not yet import `django.conf.settings`.  But you get the `site`
        object being instantiated.

        Parameters:

        :site:       The :class:`Site` instance
        :app_label:  e.g. "contacts"
        :app_name:   e.g. "lino_xl.lib.contacts"
        :app_module: The module object corresponding to the
                     :xfile:`__init__.py` file.

        """
        # site.logger.info("20140226 Plugin.__init__() %s",
        #                  app_label)
        assert not site._startup_done
        self.site = site
        self.app_name = app_name
        self.app_label = app_label
        self.app_module = app_module
        self.needed_by = needed_by
        if self.verbose_name is None:
            self.verbose_name = app_label.title()
        if self.short_name is None:
            self.short_name = self.verbose_name
        self.configure(**configs)
        self.on_init()
        # import pdb; pdb.set_trace()
        # super(Plugin, self).__init__()

    def is_active(self):
        return self._active

    def deactivate(self):
        assert not self.site._startup_done
        self._active = False

    def configure(self, **kw):
        """
        Set the given parameter(s) of this Plugin instance.  Any number of
        parameters can be specified as keyword arguments.

        Raise an exception if caller specified a key that does not
        have a corresponding attribute.
        """
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def get_required_plugins(self):
        """Return a list of names of plugins needed by this plugin.

        The default implementation returns :attr:`needs_plugins`.

        Lino will automatically install these plugins if necessary.

        Note that Lino will add them *before* your plugin.

        Note that only the app_label (not the whole plugin name) is used when
        testing whether a plugin is installed. IOW if a plugin says it requires
        a plugin "stdlib.foo" and an application already has some plugin
        "mylib.foo" installed, then "mylib.foo" satisfies "stdlib.foo".

        """

        return self.needs_plugins

    def get_used_libs(self, html=None):
        """

        Yield a series of tuples `(verbose_name, version, url)` that describe
        the libraries used by this Lino site.

        """
        return []

    def get_site_info(self, ar=None):
        return ""

    def on_init(self):
        """
        This will be called when the Plugin is being instantiated (i.e.
        even before the :class:`Site` instantiation has finished. Used
        by :mod:`lino.modlib.users` to set :attr:`user_model`.
        """
        pass

    def on_plugins_loaded(self, site):
        """
        Called exactly once on each installed plugin, when the
        :class:`Site` has loaded all plugins, but *before* calling
        :meth:`setup_plugins`.  All this happens before settings are
        ready and long before the models modules start to load.

        This is used for initializing default values of plugin
        attributes that (a) depend on other plugins but (b) should be
        overridable in :meth:`lino.core.site.Site.setup_plugins`.

        For example :mod:`groups` uses this to set a default value to
        the :attr:`commentable_model` for :mod:`comments` plugin.

        Or :mod:`lino.modlib.checkdata` uses it to set
        `responsible_user` to "robin" when it is a demo site.
        """
        pass

    def on_site_startup(self, site):
        """
        This is called exactly once when models are ready.
        """
        pass

    def before_actors_discover(self):
        """

        This is called exactly once during :term:`site startup`, when models are
        ready.  Used by `lino.modlib.help`

        """
        pass

    # def after_discover(self):
    #     """
    #     This is called exactly once during startup, when actors have been
    #     discovered. Needed by :mod:`lino.modlib.help`.
    #     """
    #     pass

    def post_site_startup(self, site):
        """
        This will be called exactly once, when models are ready.
        """
        pass

    def get_migration_steps(self, sources):
        return []

    @classmethod
    def extends_from(cls):
        """Return the plugin from which this plugin inherits."""
        # for p in self.__class__.__bases__:
        for p in cls.__bases__:
            if issubclass(p, Plugin):
                return p
        # raise Exception("20140825 extends_from failed")

    @classmethod
    def get_subdir(cls, name):
        """Get the absolute path of the named subdirectory if it exists."""
        p = dirname(inspect.getfile(cls))
        p = abspath(join(p, name))
        if isdir(p):
            return p
        # print("20150331 %s : no directory %s" % (cls, p))

    def before_analyze(self):
        """
        This is called during startup, when all models modules have been
        imported, and before Lino starts to analyze them.
        """
        pass

    def on_ui_init(self, kernel):
        """
        This is called when the kernel is being instantiated.
        """
        pass

    def __repr__(self):
        l = []
        for k in ('media_name', 'media_base_url', 'extends_models'):
            v = getattr(self, k, None)
            if v:
                l.append('{}={}'.format(k, v))
        if self.needed_by:
            l.append('needed_by={}'.format(self.needed_by.app_name))
        if self.needs_plugins:
            # l.append('needs_plugins={}'.format([p.app_name for p in self.needs_plugins]))
            l.append('needs_plugins={}'.format(self.needs_plugins))
        if len(l) == 0:
            return self.app_name
        # print(l)
        attrs = ', '.join(l)
        return "{} ({})".format(self.app_name, attrs)

    def get_patterns(self):
        """
        Override this to return a list of url patterns to be added to the
        Site's patterns.
        """
        return []

    def get_requirements(self, site) -> Iterable[str]:
        """
        Return a list of optionally required Python packages to be installed
        during :manage:`install`.

        See also :doc:`/topics/requirements`.
        """
        return []

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        """
        Yield or return a list of textlines to add to the `<head>` of the
        html page.
        """
        return []

    def get_body_lines(cls, site, request):
        return []

    def get_row_edit_lines(self, e, panel):
        return []

    def on_initdb(self, site, force=False, verbosity=1):
        """
        This is called during SITE.build_site_cache().
        """
        pass

    def build_static_url(self, *parts, **kw):
        raise Exception("Renamed to build_lib_url")

    def build_lib_url(self, *parts, **kw):
        if self.media_base_url:
            url = self.media_base_url + '/'.join(parts)
            if len(kw):
                url += "?" + urlencode(kw)
            return url
        return self.site.build_static_url(self.media_name, *parts, **kw)

    def buildurl(self, *args, **kw):
        if self.url_prefix:
            return self.site.buildurl(self.url_prefix, *args, **kw)
        return self.site.buildurl(*args, **kw)

    build_plain_url = buildurl

    def get_menu_group(self):
        """
        Return the plugin (a :class:`Plugin` instance) into the menu of which
        this plugin should add its menu commands.

        This returns `self` by default, unless

        - this plugin defines an explicit :attr:`menu_group`. In this
          case return the named plugin.

        - this plugin was automatically installed because some other
          plugin needs it. In this case return that other plugin.

        When a plugin A is automatically being installed because
        needed by a plugin B which is itself being installed
        automatically because needed by a third plugin C, then
        :meth:`A.get_menu_group
        <lino.core.plugins.Plugin.get_menu_group>` returns C (and not
        B).  A case where this happens is
        :mod:`lino_welfare.modlib.pcsw` which needs
        :mod:`lino_xl.lib.coachings` which in turn needs
        :mod:`lino_xl.lib.clients`.
        """
        if self.menu_group:
            if self.menu_group in self.site.plugins:
                return self.site.plugins.get(self.menu_group)

        needed_by = self
        while needed_by.needed_by is not None:
            needed_by = needed_by.needed_by
        return needed_by

    def setup_user_prefs(self, up):
        """
        Called when a :class:`lino.core.userprefs.UserPrefs` get
        instantiated.
        """
        pass

    def get_quicklinks(self):
        """

        Return or yield a sequence of quick link descriptors to be added to the
        list of quick links.

        A :term:`quick link` descriptor is a string that identifies either an
        actor or a bound action.

        """
        return []

    def setup_quicklinks(self, tb):
        """
        Add quicklinks to the list of quick links.
        """
        pass

    def get_dashboard_items(self, user):
        """Return or yield a sequence of items to be rendered on the
        dashboard.

        Called by :meth:`lino.core.site.Site.get_dashboard_items`.

        Every item is expected to be either an instance of
        :class:`lino.core.dashboard.DashboardItem`, or a
        :class:`lino.core.actors.Actor`.

        Tables are shown with a limit of
        :attr:`lino.core.tables.AbstractTable.preview_limit` rows.

        """
        return []

    def setup_layout_element(self, el):
        pass

    def get_detail_url(self, ar, actor, pk, *args, **kw):
        """
        Return the URL to the given database row.

        This is only a relative URL. Get the fully qualified URI by prefixing
        :attr:`lino.core.site.Site.server_url`.

        The extjs frontend overrides this and returns different URIs depending
        on whether `ar.request` is set or not.

        """
        from lino.core.renderer import TextRenderer
        if ar.renderer.__class__ is TextRenderer:
            return "Detail"  # many doctests depend on this
        parts = ['api']
        if getattr(actor.model, "_meta", False):
            parts += [actor.model._meta.app_label,
                      actor.model.get_default_table().__name__]
        else:
            parts += [actor.app_label, actor.__name__]
        parts.append(str(pk))
        parts += args
        return self.build_plain_url(*parts, **kw)

    @classmethod
    def setup_site_features(cls, site):
        pass

# if not hasattr(Plugin, 'features'):
#     for name, value in FEATURES_HOOKS.items():
#         if callable(value):
#             setattr(Plugin, name, classmethod(value))
#         else:
#             setattr(Plugin, name, value)
