# -*- coding: UTF-8 -*-
# Copyright 2013-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.utils.translation import gettext_lazy as _

from lino.modlib.users.choicelists import UserTypes
from lino.modlib.office.roles import OfficeUser
from lino.modlib.publisher.mixins import Publishable
from lino.modlib.publisher.choicelists import PublisherViews
from lino.modlib.memo.mixins import BabelPreviewable
from lino_xl.lib.cal.models import *
from lino_xl.lib.courses.choicelists import EnrolmentStates



class Room(Room, Publishable, BabelPreviewable):

    class Meta(Room.Meta):
        abstract = dd.is_abstract_model(__name__, 'Room')


class Rooms(Rooms):
    column_names = "name company company__city *"
    detail_layout = """
    id name
    company contact_person contact_role
    cal.EntriesByRoom
    """

PublisherViews.add_item_lazy("rooms", Rooms)


class Event(Event, Publishable, BabelPreviewable):

    class Meta(Event.Meta):
        abstract = dd.is_abstract_model(__name__, 'Event')


class MyEntries(MyEntries):
    column_names = 'when_text detail_link #summary room owner workflow_buttons *'
