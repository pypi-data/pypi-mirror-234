# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This is the main module of Lino Cms.

.. autosummary::
   :toctree:

   lib


"""

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO.get('version')

intersphinx_urls = dict(docs="https://lino-framework.gitlab.io/cms")
srcref_url = 'https://gitlab.com/lino-framework/cms/blob/master/%s'
doc_trees = ['docs']
