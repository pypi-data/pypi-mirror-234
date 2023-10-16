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
Member Views
"""

from webhelpers2.html import tags

from tailbone.views import ViewSupplement


class MembershipTypeViewSupplement(ViewSupplement):
    """
    MembershipType view supplement for CORE integration
    """
    route_prefix = 'membership_types'

    def get_xref_buttons(self, memtype):
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        url = corepos.get_office_url()
        if url:
            url = f'{url}/mem/MemberTypeEditor.php'
            return [{'url': url, 'text': "View in CORE Office"}]


class MemberViewSupplement(ViewSupplement):
    """
    Member view supplement for CORE integration
    """
    route_prefix = 'members'

    labels = {
        'corepos_account_id': "CORE-POS Account ID",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreMember)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('corepos_account_id', model.CoreMember.corepos_account_id)

    def configure_form(self, f):
        f.append('corepos_account_id')

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreMember]

    def get_xref_buttons(self, member):
        if member.customer and member.customer.corepos_card_number:
            app = self.get_rattail_app()
            corepos = app.get_corepos_handler()
            url = corepos.get_office_member_url(member.customer.corepos_card_number)
            if url:
                return [{'url': url, 'text': "View in CORE Office"}]

    def get_xref_links(self, member):
        if member.customer and member.customer.corepos_card_number:
            url = self.request.route_url('corepos.members.view',
                                         card_number=member.customer.corepos_card_number)
            return [tags.link_to("View CORE-POS Member", url)]


class MemberEquityPaymentViewSupplement(ViewSupplement):
    """
    Member view supplement for CORE integration
    """
    route_prefix = 'member_equity_payments'

    labels = {
        'corepos_card_number': "CORE-POS Card Number",
        'corepos_transaction_number': "CORE-POS Transaction Number",
        'corepos_transaction_id': "CORE-POS Transaction ID",
        'corepos_department_number': "CORE-POS Department Number",
        'corepos_datetime': "CORE-POS Date/Time",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreMemberEquityPayment)

    def configure_grid(self, g):
        model = self.model

        g.set_filter('corepos_card_number', model.CoreMemberEquityPayment.corepos_card_number)
        g.set_sorter('corepos_card_number', model.CoreMemberEquityPayment.corepos_card_number)

        g.set_filter('corepos_transaction_number', model.CoreMemberEquityPayment.corepos_transaction_number)
        g.set_sorter('corepos_transaction_number', model.CoreMemberEquityPayment.corepos_transaction_number)

        g.set_filter('corepos_transaction_id', model.CoreMemberEquityPayment.corepos_transaction_id)
        g.set_sorter('corepos_transaction_id', model.CoreMemberEquityPayment.corepos_transaction_id)

        g.set_filter('corepos_department_number', model.CoreMemberEquityPayment.corepos_department_number)
        g.set_sorter('corepos_department_number', model.CoreMemberEquityPayment.corepos_department_number)

        g.append('corepos_transaction_number')
        g.set_label('corepos_transaction_number', "CORE-POS Trans. No.")
        if 'corepos_transaction_number' in g.filters:
            g.filters['corepos_transaction_number'].label = self.labels['corepos_transaction_number']
        g.set_link('corepos_transaction_number')

        # corepos_datetime
        g.append('corepos_datetime')
        g.set_type('corepos_datetime', 'datetime')
        g.set_filter('corepos_datetime', model.CoreMemberEquityPayment.corepos_datetime)
        g.set_sorter('corepos_datetime', model.CoreMemberEquityPayment.corepos_datetime)

    def configure_form(self, f):

        f.append('corepos_card_number')
        f.set_readonly('corepos_card_number')

        f.append('corepos_transaction_number')
        f.set_readonly('corepos_transaction_number')

        f.append('corepos_transaction_id')
        f.set_readonly('corepos_transaction_id')

        f.append('corepos_department_number')
        f.set_readonly('corepos_department_number')

        f.append('corepos_datetime')
        f.set_readonly('corepos_datetime')

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreMemberEquityPayment]

    def get_xref_buttons(self, payment):
        if payment.corepos_transaction_number and payment.corepos_card_number:
            app = self.get_rattail_app()
            corepos = app.get_corepos_handler()
            url = corepos.get_office_url()
            if url:
                url = f'{url}/reports/Equity/EquityReport.php?memNum={payment.corepos_card_number}'
                return [{'url': url, 'text': "View in CORE Office"}]


def includeme(config):
    MembershipTypeViewSupplement.defaults(config)
    MemberViewSupplement.defaults(config)
    MemberEquityPaymentViewSupplement.defaults(config)
