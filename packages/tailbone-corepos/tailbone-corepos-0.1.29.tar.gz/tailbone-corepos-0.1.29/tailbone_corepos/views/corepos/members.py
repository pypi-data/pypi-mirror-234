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
CORE-POS member views
"""

from sqlalchemy import orm

from corepos.db.office_op import model as corepos
from corepos.db.office_trans import model as coretrans

from webhelpers2.html import HTML, tags

from tailbone_corepos.db import CoreTransSession
from .master import CoreOfficeMasterView


class MemberTypeView(CoreOfficeMasterView):
    """
    Master view for member types
    """
    model_class = corepos.MemberType
    model_title = "CORE-POS Member Type"
    url_prefix = '/core-pos/member-types'
    route_prefix = 'corepos.member_types'

    labels = {
        'id': "ID",
        'ssi': "SSI",
    }

    def configure_grid(self, g):
        super(MemberTypeView, self).configure_grid(g)

        g.set_link('id')
        g.set_link('description')


class MemberView(CoreOfficeMasterView):
    """
    Master view for members
    """
    model_class = corepos.MemberInfo
    model_title = "CORE-POS Member (classic)"
    model_title_plural = "CORE-POS Members (classic)"
    url_prefix = '/core-pos/members'
    route_prefix = 'corepos.members'

    labels = {
        'card_number': "Card No.",
        'email2': "Email 2",
        'ads_ok': "Ads OK",
    }

    grid_columns = [
        'card_number',
        'first_name',
        'last_name',
        'street',
        'city',
        'state',
        'zip',
        'phone',
        'email',
    ]

    form_fields = [
        'card_number',
        'first_name',
        'last_name',
        'other_first_name',
        'other_last_name',
        'customers',
        'street',
        'city',
        'state',
        'zip',
        'phone',
        'email',
        'email2',
        'ads_ok',
        'dates',
        'barcodes',
        'suspension',
        'equity_live_balance',
    ]

    has_rows = True
    model_row_class = coretrans.StockPurchase
    rows_title = "Stock Purchases"

    row_labels = {
        'transaction_id': "Transaction ID",
    }

    row_grid_columns = [
        'datetime',
        'amount',
        'transaction_number',
        'transaction_id',
        'department_number',
    ]

    def configure_grid(self, g):
        super(MemberView, self).configure_grid(g)

        g.set_sort_defaults('card_number')

        g.filters['card_number'].default_active = True
        g.filters['card_number'].default_verb = 'equal'

        g.set_link('card_number')
        g.set_link('first_name')
        g.set_link('last_name')

    def configure_form(self, f):
        super(MemberView, self).configure_form(f)

        f.set_renderer('dates', self.render_member_dates)

        f.set_renderer('barcodes', self.render_barcodes)

        f.set_readonly('customers')
        f.set_renderer('customers', self.render_customers)

        f.set_renderer('suspension', self.render_suspension)

        f.set_renderer('equity_live_balance', self.render_equity_live_balance)

    def render_member_dates(self, member, field):
        if not member.dates:
            return ""

        items = []
        for dates in member.dates:
            items.append(HTML.tag('li', c=str(dates)))
        return HTML.tag('ul', c=items)

    def render_barcodes(self, member, field):
        barcodes = member.barcodes
        if not barcodes:
            return

        items = []
        for barcode in barcodes:
            if barcode.upc:
                text = barcode.upc
            elif barcode.upc is None:
                text = "(null)"
            else:
                text = "(empty string)"
            items.append(HTML.tag('li', c=[text]))
        return HTML.tag('ul', c=items)

    def render_customers(self, member, field):
        customers = member.customers
        if not customers:
            return

        items = []
        for customer in customers:
            text = str(customer)
            url = self.request.route_url('corepos.customers.view',
                                         id=customer.id)
            link = tags.link_to(text, url)
            items.append(HTML.tag('li', c=[link]))
        return HTML.tag('ul', c=items)

    def render_suspension(self, member, field):
        suspension = member.suspension
        if not suspension:
            return

        text = str(suspension)
        url = self.request.route_url('corepos.suspensions.view',
                                     card_number=suspension.card_number)
        return tags.link_to(text, url)

    def render_equity_live_balance(self, member, field):
        try:
            balance = CoreTransSession.query(coretrans.EquityLiveBalance)\
                                      .filter(coretrans.EquityLiveBalance.member_number == member.card_number)\
                                      .one()
        except orm.exc.NoResultFound:
            return

        app = self.get_rattail_app()
        return app.render_currency(balance.payments)

    def get_xref_buttons(self, member):
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        url = corepos.get_office_member_url(member.card_number)
        if url:
            return [self.make_xref_button(url=url, text="View in CORE Office")]

    def get_row_data(self, member):
        return CoreTransSession.query(coretrans.StockPurchase)\
                               .filter(coretrans.StockPurchase.card_number == member.card_number)

    def get_parent(self, stock_purchase):
        return self.Session.get(corepos.MemberInfo, stock_purchase.card_number)

    def configure_row_grid(self, g):
        super().configure_row_grid(g)

        g.set_type('amount', 'currency')

        g.set_sort_defaults('datetime', 'desc')

    def row_view_action_url(self, stock_purchase, i):
        return self.request.route_url('corepos.stock_purchases.view',
                                      card_number=stock_purchase.card_number,
                                      datetime=stock_purchase.datetime,
                                      transaction_number=stock_purchase.transaction_number,
                                      department_number=stock_purchase.department_number)


def defaults(config, **kwargs):
    base = globals()

    MemberTypeView = kwargs.get('MemberTypeView', base['MemberTypeView'])
    MemberTypeView.defaults(config)

    MemberView = kwargs.get('MemberView', base['MemberView'])
    MemberView.defaults(config)


def includeme(config):
    defaults(config)
