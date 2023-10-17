# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Database models specific for Lino Noi.

Defines a customized :class:`TicketDetail`.

"""

import logging ; logger = logging.getLogger(__name__)

from lino.api import _
from lino.mixins.sequenced import Hierarchical
from lino.modlib.users.mixins import Assignable
from lino_xl.lib.tickets.models import *
from lino_xl.lib.working.mixins import SummarizedFromSession
from lino_xl.lib.working.choicelists import ReportingTypes, ZERO_DURATION
from lino.modlib.search.mixins import ElasticSearchable


def get_summary_fields():
    for t in ReportingTypes.get_list_items():
        yield t.name + '_hours'

class Site(Site):

    class Meta(Site.Meta):
        app_label = 'tickets'
        abstract = dd.is_abstract_model(__name__, 'Site')

    def get_change_observers(self, ar=None):
        for s in rt.models.groups.Group.objects.filter(site=self):
            for sub in s.members.all():
                yield (sub.user, sub.user.mail_mode)


class Ticket(Ticket, Assignable, SummarizedFromSession, Hierarchical, ElasticSearchable):

    class Meta(Ticket.Meta):
        # app_label = 'tickets'
        abstract = dd.is_abstract_model(__name__, 'Ticket')

    ES_indexes = [(
        'ticket',
        {
            "mappings": {
                "properties": {
                    "closed": {
                        "type": "boolean"
                    },
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "autocomplete",
                        "search_analyzer": "autocomplete_search"
                    },
                    "end_user": {
                        "type": "long"
                    },
                    "feedback": {
                        "type": "boolean"
                    },
                    "model": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "autocomplete",
                        "search_analyzer": "autocomplete_search"
                    },
                    "priority": {
                        "type": "long"
                    },
                    "private": {
                        "type": "boolean"
                    },
                    "site": {
                        "type": "long"
                    },
                    "standby": {
                        "type": "boolean"
                    },
                    "state": {
                        "properties": {
                            "text": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            },
                            "value": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            }
                        }
                    },
                    "summary": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "autocomplete",
                        "search_analyzer": "autocomplete_search"
                    },
                    "ticket_type": {
                        "type": "long"
                    },
                    "upgrade_notes": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "autocomplete",
                        "search_analyzer": "autocomplete_search"
                    },
                    "user": {
                        "type": "long"
                    },
                    "waiting_for": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "autocomplete",
                        "search_analyzer": "autocomplete_search"
                    }
                }
            }
        }
    )]

    if dd.is_installed('notify'):
        def assigned_to_changed(self, ar):
            """Send notification of assignment"""

            if (self.assigned_to is not None and self.assigned_to != ar.user):
                ctx = dict(user=ar.user, what=self.obj2memo())
                def msg(user, mm):
                    subject = _("{user} has assigned you to ticket: {what}").format(**ctx)
                    return (subject , tostring(E.span(subject)))

                mt = rt.models.notify.MessageTypes.tickets

                rt.models.notify.Message.emit_notification(
                    ar, self, mt, msg,
                    [(self.assigned_to, self.assigned_to.mail_mode)]
                )

    # show_commits = dd.ShowSlaveTable('github.CommitsByTicket')
    show_changes = dd.ShowSlaveTable('changes.ChangesByMaster')
    # show_wishes = dd.ShowSlaveTable('deploy.DeploymentsByTicket')
    # show_stars = dd.ShowSlaveTable('stars.AllStarsByController')


    def get_change_subject(self, ar, cw):
        ctx = dict(user=ar.user, what=str(self))
        if cw is None:
            # return _("{user} submitted ticket {what}").format(**ctx)
            return
        if len(list(cw.get_updates())) == 0:
            return
        return _("{user} modified {what}").format(**ctx)

    def get_change_body(self, ar, cw):
        # ctx = dict(user=ar.user, what=self.obj2memo())
        ctx = dict(user=ar.user, what=ar.obj2htmls(self))
        if cw is None:
            html = _("{user} submitted ticket {what}").format(**ctx)
            html = "<p>{}</p>.".format(html)
        else:
            items = list(cw.get_updates_html(["_user_cache"]))
            if len(items) == 0:
                return
            html = _("{user} modified {what}").format(**ctx)
            html = "<p>{}:</p>".format(html)
            html += tostring(E.ul(*items))
        return "<div>{}</div>".format(html)

    @classmethod
    def get_layout_aliases(cls):
        yield ("SUMMARY_FIELDS", ' '.join(get_summary_fields()))

    # @classmethod
    # def get_summary_master_model(cls):
    #     return cls

    def reset_summary_data(self):
        for k in get_summary_fields():
            setattr(self, k, ZERO_DURATION)
        self.last_commenter = None

    def get_summary_collectors(self):
        qs = rt.models.working.Session.objects.filter(ticket=self)
        yield (self.add_from_session, qs)
        qs = rt.models.comments.Comment.objects.filter(**gfk2lookup(rt.models.comments.Comment._meta.get_field("owner"),
                                                                    self)
                                                       ).order_by("-created")[0:1]
        yield (self.add_from_comment, qs)

    def add_from_comment(self, obj):
        self.last_commenter = obj.user

    @dd.chooser()
    def site_choices(cls, ar):
        # if user is None:
        #     user = ar.get_user()
        user = ar.get_user()
        # user = user if user is not None else ar.get_user()
        group_ids = rt.models.groups.Membership.objects.filter(user=user).values_list("group__pk", flat=True)
        # user_ids = [user.pk]
        # if end_user: user_ids.append(end_user.pk)
        # pks = rt.models.tickets.Subscription.objects.filter(user__pk__in=user_ids).values_list("site__pk", flat=True)
        # # print(pks)
        # return Site.objects.filter(id__in=pks)
        return Site.objects.filter(group__in=group_ids)


class TicketDetail(TicketDetail):
    """Customized detail_layout for Tickets in Noi

    """
    main = "general_tab more_tab links #history_tab #more2 #github.CommitsByTicket"

    general_tab = dd.Panel("""
    general1:30 general2:30 general3:30
    """, label=_("General"))


    # 50+6=56
    # in XL: label span is 4, so we have 8 units for the fields
    # 56.0/8 = 7
    # summary:  50/56*8 = 7.14 --> 7
    # id:  6/56*8 = 0.85 -> 1
    general1 = """
    overview
    """
    general2 = """
    order end_user ticket_type
    triager_panel
    priority:10 planned_time deadline
    SUMMARY_FIELDS
    working.SessionsByTicket
    """

    triager_panel = dd.Panel(
    """
    site quick_assign_to private:10
    """, required_roles=dd.login_required(Triager))

    general3 = """
    workflow_buttons
    comment
    comments.CommentsByRFC:30
    """

    more_tab = dd.Panel("""
    more1 more2 more3
    """, label=_("More"))

    # history_tab = dd.Panel("""
    # changes.ChangesByMaster #stars.StarsByController:20
    # github.CommitsByTicket
    # """, label=_("History"), required_roles=dd.login_required(Triager))

    more1 = """
    id:6 ref
    summary
    # standby feedback closed
    description
    """

    more2 = """
    upgrade_notes
    uploads.UploadsByController
    # tickets.CheckListItemsByTicket
    """

    more3 = """
    state
    assigned_to
    user created
    modified fixed_since
    duplicate_of
    DuplicatesByTicket:20
    """

    # more1 = """
    # created modified fixed_since #reported_for #fixed_date #fixed_time
    # state assigned_to ref duplicate_of deadline
    # # standby feedback closed
    # """

    # more2 = dd.Panel("""
    # # deploy.DeploymentsByTicket
    # # skills.DemandsByDemander
    # stars.AllStarsByController
    # uploads.UploadsByController
    # """, label=_("Even more"))

    links = dd.Panel("""
    links_left comments.CommentsByMentioned #LinksByTicket
    """, label=_("Links"))

    links_left = """
    parent
    TicketsByParent
    """

class TicketInsertLayout(dd.InsertLayout):
    main = """
    summary #private:20
    right:30 left:50
    """

    right = """
    ticket_type
    priority
    end_user
    #assigned_to
    site
    """

    left = """
    description
    """

    window_size = (80, 20)


class SiteDetail(SiteDetail):

    main = """general config"""

    general = dd.Panel("""
    gen_left:20 TicketsBySite:60
    """, label=_("General"))

    gen_left = """
    group
    overview
    """

    general2 = """
    ref name
    company contact_person
    reporting_type #start_date end_date hours_paid
    remark:20 private
    workflow_buttons:20 id
    working.SummariesBySite
    """

    config = dd.Panel("""
    general2:50 description:30
    """, label=_("Configure"), required_roles = dd.login_required(TicketsStaff))

    # history = dd.Panel("""
    # # meetings.MeetingsBySite
    # working.SummariesBySite
    # """, label=_("History"))


# Note in the following lines we don't subclass Tickets because then
# we would need to also override these attributes for all subclasses

Tickets.insert_layout = 'tickets.TicketInsertLayout'
Tickets.params_layout = """user end_user assigned_to not_assigned_to interesting_for site has_site state priority
    #deployed_to show_assigned show_active #show_deployed show_todo show_private
    start_date end_date observed_event #topic #feasable_by has_ref
    last_commenter not_last_commenter subscriber"""
Tickets.column_names = 'id summary:50 #user:10 #topic #faculty priority ' \
                       'workflow_buttons:30 site:10 #project:10'
Tickets.tablet_columns = "id summary workflow_buttons"
#Tickets.tablet_columns_popin = "site project"

Tickets.mobile_columns = "workflow_buttons"
#Tickets.mobile_columns_pop = "summary workflow_buttons"
Tickets.popin_columns = "summary"

Tickets.order_by = ["-id"]

TicketsBySite.column_names = "priority detail_link workflow_buttons planned_time SUMMARY_FIELDS *"
AllSites.column_names = "ref name company group remark workflow_buttons id *"
# Sites.detail_layout = """
# id name partner #responsible_user
# remark
# #InterestsBySite TicketsBySite deploy.MilestonesBySite
# """


class TicketsByParent(Tickets):
    required_roles = dd.login_required(Reporter)
    # label = _("Known problems")
    master_key = 'parent'
    column_names = "priority id summary:50 quick_assign_to #ticket_type #workflow_buttons *"
    details_of_master_template = _("Children of %(master)s")


from lino.modlib.checkdata.choicelists import Checker

class TicketOrderChecker(Checker):
    # Can be removed when all production sites have upgraded to lino-noi>=22.12
    verbose_name = _("Fill the new 'order' field")
    model = Ticket

    def get_checkdata_problems(self, obj, fix=False):
        if obj.site_id is None:
            return
        if obj.site.ref is None:
            return
        # if obj.site.company == settings.SITE.site_config.site_company:
        #     return

        cust = obj.site.ref.startswith("cust.")
        if not cust:
            if obj.order_id is not None:
                yield (True, _("Order should be empty (not a customer project)"))
                if fix:
                    obj.order = None
                    obj.full_clean()
                    obj.save()
                    # logger.info("Removed order because its not a customer project", obj)
            return

        if obj.order_id and obj.order.ref == obj.site.ref:
            return
        yield (True, _("Must populate order from project"))
        if fix:
            # Not tested. We'll just get it work after the upgrade
            Subscription = rt.models.subscriptions.Subscription
            Journal = rt.models.ledger.Journal
            VoucherTypes = rt.models.ledger.VoucherTypes
            TradeTypes = rt.models.ledger.TradeTypes
            sub = Subscription.get_by_ref(obj.site.ref, None)
            if sub is None:
                jnl = Journal.get_by_ref('SLA', None)
                if jnl is None:
                    vt = VoucherTypes.get_for_model(Subscription)
                    jnl = Journal(ref="SLA", voucher_type=vt,
                        trade_type=TradeTypes.sales,
                        journal_group="sales",
                        **dd.str2kw("name", _("Service Level Agreements")))
                    jnl.full_clean()
                    jnl.save()
                sub = Subscription(partner=obj.site.company, journal=jnl, ref=obj.site.ref)
                sub.full_clean()
                sub.save()
            obj.order = sub
            obj.full_clean()
            obj.save()
            logger.info("Filled %s order field after upgrade to Noi 22.12", obj)

TicketOrderChecker.activate()
