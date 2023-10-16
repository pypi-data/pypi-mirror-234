# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.projects.std.settings import *
from lino_cms import SETUP_INFO

class Site(Site):

    verbose_name = "Lino CMS"
    description = SETUP_INFO['description']
    version = SETUP_INFO['version']
    url = SETUP_INFO['url']

    demo_fixtures = ['std', 'demo', 'demo2', 'checkdata']
    user_types_module = 'lino_cms.lib.cms.user_types'
    custom_layouts_module = 'lino_cms.lib.cms.layouts'
    migration_class = 'lino_cms.lib.cms.migrate.Migrator'
    default_ui = "lino_react.react"

    def setup_features(self):
        super().setup_features()
        self.enable_feature('third_party_authentication')

    def get_installed_apps(self):
        """Implements :meth:`lino.core.site.Site.get_installed_apps`.

        """
        yield super(Site, self).get_installed_apps()
        yield 'lino_cms.lib.cms'
        yield 'lino_cms.lib.users'
        yield 'lino_xl.lib.contacts'
        # yield 'lino_cms.lib.cal'
        # yield 'lino_xl.lib.calview'
        yield 'lino_xl.lib.pages'
        yield 'lino_xl.lib.blogs'
        yield 'lino_xl.lib.albums'
        yield 'lino.modlib.comments'
        # yield 'lino.modlib.uploads'
        yield 'lino.modlib.help'
        yield 'lino.modlib.publisher'
        yield 'lino.modlib.checkdata'  # fill body_preview during prep

    # def setup_quicklinks(self, ut, tb):
    #     super(Site, self).setup_quicklinks(ut, tb)

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        # yield ('system', 'use_dashboard_layouts', True)
        yield ('users', 'allow_online_registration', True)
        # yield ('cal', 'with_demo_appointments', False)
        yield ('help', 'make_help_pages', True)
        yield ('help', 'use_contacts', True)
        yield ('help', 'include_useless', True)
        yield ('memo', 'short_preview_length', 600)

from lino.core.auth.utils import activate_social_auth_testing
activate_social_auth_testing(globals())
