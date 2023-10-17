# -*- coding: UTF-8 -*-
# Copyright 2015-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Defines a set of user roles and fills
:class:`lino.modlib.users.choicelists.UserTypes`.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for :ref:`noi`.
"""

from django.utils.translation import gettext_lazy as _

from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.users.roles import Helper
from lino.modlib.comments.roles import CommentsUser, CommentsStaff, PrivateCommentsReader, CommentsReader
from lino.core.roles import SiteUser, SiteAdmin, Expert, DataExporter
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.tickets.roles import Reporter, Searcher, Triager, TicketsStaff
from lino_xl.lib.working.roles import Worker
from lino_xl.lib.cal.roles import CalendarReader
from lino_xl.lib.votes.roles import VotesStaff, VotesUser
from lino_xl.lib.products.roles import ProductsStaff
from lino_xl.lib.ledger.roles import LedgerStaff
from lino_xl.lib.invoicing.roles import InvoicingUser, InvoicingStaff
from lino_xl.lib.storage.roles import StorageUser, StorageStaff


from lino.modlib.users.choicelists import UserTypes


class Customer(SiteUser, OfficeUser, VotesUser, Searcher, Reporter,
        CommentsUser, DataExporter):
    """
    A **Customer** is somebody who uses our software and may report
    tickets, but won't work on them. Able to comment and view tickets on sites
    they are member of. Unable to see any contact data of other users or partners.
    """
    pass


class Contributor(Customer, Searcher, Helper, Worker, ExcerptsUser, CoursesUser):
    """
    A **Contributor** is somebody who works on tickets of sites they are team members of.
    """
    pass


class Developer(Contributor, Expert, ContactsUser, Triager, ExcerptsStaff, CommentsStaff, TicketsStaff, PrivateCommentsReader):
    """
    A **Developer** is a trusted user who has signed an NDA. Has access to client contacts.
    Is able to make service reports as well as manage tickets.
    """
    pass


class SiteAdmin(
    SiteAdmin, Developer, OfficeStaff, VotesStaff, ContactsStaff,
    CommentsStaff, ProductsStaff, LedgerStaff, InvoicingStaff, StorageStaff):
    """
    Can do everything.
    """


# class Anonymous(CommentsReader, CalendarReader):
class Anonymous(CalendarReader, CommentsReader, Searcher):
    pass


UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), Anonymous, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("Customer"), Customer, 'customer user')
add('200', _("Contributor"), Contributor, 'contributor')
add('400', _("Developer"), Developer, 'developer')
add('900', _("Administrator"), SiteAdmin, 'admin')


from lino_xl.lib.storage.choicelists import StorageStates
StorageStates.clear()
add = StorageStates.add_item
add('10', _("Purchased"), 'purchased')
