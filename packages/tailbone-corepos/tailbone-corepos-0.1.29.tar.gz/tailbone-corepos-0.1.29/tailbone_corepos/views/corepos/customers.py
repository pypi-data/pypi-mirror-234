# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE POS customer views
"""

from corepos.db.office_op import model as corepos

from webhelpers2.html import tags

from .master import CoreOfficeMasterView


def render_member_info(request, custdata, field):
    meminfo = custdata.member_info
    if not meminfo:
        return
    text = str(meminfo)
    url = request.route_url('corepos.members.view',
                            card_number=meminfo.card_number)
    return tags.link_to(text, url)


class CustomerClassicView(CoreOfficeMasterView):
    """
    Master view for "classic" customers, i.e. ``custdata`` table
    """
    model_class = corepos.CustomerClassic
    model_title = "CORE-POS Customer (classic)"
    model_title_plural = "CORE-POS Customers (classic)"
    url_prefix = '/core-pos/customers'
    route_prefix = 'corepos.customers'
    results_downloadable = True
    set_deletable = True
    mergeable = True

    labels = {
        'id': "ID",
        'card_number': "Card No.",
        'person_number': "Person No.",
        'charge_ok': "Charge OK",
        'member_type_id': "Member Type No.",
        'number_of_checks': "Number of Checks",
        'ssi': "SSI",
    }

    grid_columns = [
        'card_number',
        'person_number',
        'first_name',
        'last_name',
        'member_type',
        'ssi',
        'charge_ok',
        'charge_limit',
        'balance',
        'write_checks',
        'purchases',
    ]

    def query(self, session):
        query = super().query(session)

        query = query.outerjoin(corepos.MemberInfo,
                                corepos.MemberInfo.card_number == corepos.CustomerClassic.card_number)

        return query

    def configure_grid(self, g):
        super().configure_grid(g)

        g.filters['card_number'].default_active = True
        g.filters['card_number'].default_verb = 'equal'

        g.filters['first_name'].default_active = True
        g.filters['first_name'].default_verb = 'contains'

        g.filters['last_name'].default_active = True
        g.filters['last_name'].default_verb = 'contains'

        g.set_joiner('member_type_description', lambda q: q.outerjoin(corepos.MemberType))
        g.set_sorter('member_type_description', corepos.MemberType.description)
        g.set_filter('member_type_description', corepos.MemberType.description)

        g.set_filter('member_info_email', corepos.MemberInfo.email)
        g.set_filter('member_info_email2', corepos.MemberInfo.email2)

        g.set_type('charge_limit', 'currency')
        g.set_type('balance', 'currency')
        g.set_type('purchases', 'currency')

        g.set_sort_defaults('card_number')

        g.set_link('card_number')
        g.set_link('first_name')
        g.set_link('last_name')

    def get_uuid_for_grid_row(self, customer):
        # nb. uniquely identify records, for merge support
        return customer.id

    def configure_form(self, f):
        super().configure_form(f)

        f.set_renderer('member_info', self.render_member_info)
        f.set_renderer('member_type', self.render_member_type)

        if self.creating or self.editing:
            f.remove_field('member_info')
            f.remove_field('member_type')
            f.remove_field('last_change')
        else:
            f.set_type('last_change', 'datetime_local')

    def render_member_type(self, custdata, field):
        memtype = custdata.member_type
        if not memtype:
            return
        text = str(memtype)
        url = self.request.route_url('corepos.member_types.view', id=memtype.id)
        return tags.link_to(text, url)

    def render_member_info(self, custdata, field):
        return render_member_info(self.request, custdata, field)

    def core_office_object_url(self, office_url, customer):
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        return corepos.get_office_member_url(customer.card_number)

    def download_results_fields_available(self, **kwargs):
        fields = super().download_results_fields_available(**kwargs)

        fields.extend([
            'email',
            'email2',
        ])

        return fields

    def download_results_normalize(self, custdata, fields, **kwargs):
        data = super().download_results_normalize(custdata, fields, **kwargs)

        # import ipdb; ipdb.set_trace()

        for field in ('email', 'email2'):
            if field in fields:
                data[field] = getattr(custdata.member_info, field) if custdata.member_info else None

        return data


class CustomerAccountView(CoreOfficeMasterView):
    """
    Master view for "new" customer accounts, i.e. ``CustomerAccounts``
    table
    """
    model_class = corepos.CustomerAccount
    model_title = "CORE-POS Customer Account (new)"
    model_title_plural = "CORE-POS Customer Accounts (new)"
    url_prefix = '/core-pos/customer-accounts-new'
    route_prefix = 'corepos.customer_accounts_new'
    results_downloadable = True

    grid_columns = [
        'id',
        'card_number',
        'member_status',
        'active_status',
        'customer_type',
        'start_date',
        'end_date',
        'modified',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)

        g.filters['card_number'].default_active = True
        g.filters['card_number'].default_verb = 'equal'
        g.set_sort_defaults('card_number')


class CustomerView(CoreOfficeMasterView):
    """
    Master view for "new" customers, i.e. ``Customers`` table
    """
    model_class = corepos.Customer
    model_title = "CORE-POS Customer (new)"
    model_title_plural = "CORE-POS Customers (new)"
    url_prefix = '/core-pos/customers-new'
    route_prefix = 'corepos.customers_new'
    results_downloadable = True

    labels = {
        'account_id': "Account ID",
    }

    grid_columns = [
        'id',
        'account',
        'card_number',
        'first_name',
        'last_name',
        'account_holder',
        'staff',
        'modified',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)

        g.filters['card_number'].default_active = True
        g.filters['card_number'].default_verb = 'equal'
        g.set_sort_defaults('card_number')


class CustomerNotificationView(CoreOfficeMasterView):
    """
    Master view for customers notifications
    """
    model_class = corepos.CustomerNotification
    model_title = "CORE-POS Customer Notification"
    model_title_plural = "CORE-POS Customer Notifications"
    url_prefix = '/core-pos/customer-notifications'
    route_prefix = 'corepos.customer_notifications'

    labels = {
        'customer_id': "Customer ID",
    }

    def configure_grid(self, g):
        super().configure_grid(g)

        g.set_link('id')
        g.set_sort_defaults('id', 'desc')

        g.set_link('card_number')
        if 'card_number' in g.filters:
            g.filters['card_number'].default_active = True
            g.filters['card_number'].default_verb = 'equal'

        g.set_link('message')


class SuspensionView(CoreOfficeMasterView):
    """
    Master view for legacy customer suspensions.
    """
    model_class = corepos.Suspension
    model_title = "CORE-POS Suspension"
    model_title_plural = "CORE-POS Suspensions"
    url_prefix = '/core-pos/suspensions'
    route_prefix = 'corepos.suspensions'

    labels = {
        'reason_object': "Reason Code",
    }

    grid_columns = [
        'card_number',
        'type',
        'memtype1',
        'memtype2',
        'suspension_date',
        'reason',
        'mail_flag',
        'discount',
        'charge_limit',
        'reason_object',
    ]

    form_fields = [
        'card_number',
        'member_info',
        'type',
        'memtype1',
        'memtype2',
        'suspension_date',
        'reason',
        'mail_flag',
        'discount',
        'charge_limit',
        'reason_object',
    ]

    def configure_grid(self, g):
        super(SuspensionView, self).configure_grid(g)

        g.filters['card_number'].default_active = True
        g.filters['card_number'].default_verb = 'equal'

        g.set_type('charge_limit', 'currency')

        g.set_sort_defaults('card_number')

        g.set_link('card_number')

    def configure_form(self, f):
        super(SuspensionView, self).configure_form(f)

        f.set_renderer('member_info', self.render_member_info)

        f.set_type('charge_limit', 'currency')

    def render_member_info(self, custdata, field):
        return render_member_info(self.request, custdata, field)


def defaults(config, **kwargs):
    base = globals()

    CustomerClassicView = kwargs.get('CustomerClassicView', base['CustomerClassicView'])
    CustomerClassicView.defaults(config)

    CustomerAccountView = kwargs.get('CustomerAccountView', base['CustomerAccountView'])
    CustomerAccountView.defaults(config)

    CustomerView = kwargs.get('CustomerView', base['CustomerView'])
    CustomerView.defaults(config)

    CustomerNotificationView = kwargs.get('CustomerNotificationView', base['CustomerNotificationView'])
    CustomerNotificationView.defaults(config)

    SuspensionView = kwargs.get('SuspensionView', base['SuspensionView'])
    SuspensionView.defaults(config)


def includeme(config):
    defaults(config)
