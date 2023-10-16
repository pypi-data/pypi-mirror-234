# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.modlib.users.ui import *

class UserDetail(UserDetail):

    main = "general contact"

    general = dd.Panel("""
    box1
    remarks:40 users.AuthoritiesGiven:20
    """, label=_("General"))

    box1 = """
    username user_type:20
    language time_zone
    id created modified
    """

    contact = dd.Panel("""
    first_name last_name initials
    """, label=_("Contact"))

Users.detail_layout = UserDetail()

Users.column_names = "first_name email"
