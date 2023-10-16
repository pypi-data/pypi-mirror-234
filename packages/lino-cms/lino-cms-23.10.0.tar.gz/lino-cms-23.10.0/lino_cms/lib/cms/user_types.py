# -*- coding: UTF-8 -*-
# Copyright 2017-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Defines the user types for a Lino CMS.

"""

from lino.core.roles import UserRole, SiteAdmin, SiteStaff, SiteUser
from lino_xl.lib.blogs.roles import BlogsReader
from lino_xl.lib.cal.roles import CalendarReader
from lino.modlib.checkdata.roles import CheckdataUser
from lino.modlib.search.roles import SiteSearcher
from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator
from lino.modlib.uploads.roles import UploadsReader
from lino.modlib.comments.roles import CommentsUser, CommentsStaff, CommentsReader

from lino.modlib.users.choicelists import UserTypes
from django.utils.translation import gettext_lazy as _


class EndUser(BlogsReader, SiteUser, CheckdataUser, CommentsUser,
    OfficeUser, CommentsReader, CalendarReader):
    """An **end user** is somebody who uses our database, but won't work
    on it.

    """
    pass


class Staff(SiteStaff, EndUser, CommentsStaff, OfficeOperator):
    pass


class Admin(SiteAdmin, Staff, OfficeStaff):
    """Can do everything."""


# class Anonymous(CommentsReader, CalendarReader):
class Anonymous(SiteSearcher, BlogsReader, CalendarReader, UploadsReader):
    pass

UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"),        Anonymous, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"),             EndUser, 'user')
add('800', _("Staff"),            Staff, 'staff')
add('900', _("Administrator"),    Admin, 'admin')
