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
Customer Views
"""

from webhelpers2.html import tags

from tailbone.views import ViewSupplement


class CustomerViewSupplement(ViewSupplement):
    """
    Customer view supplement for CORE integration
    """
    route_prefix = 'customers'

    labels = {
        'corepos_account_id': "CORE-POS Account ID",
        'corepos_card_number': "CORE-POS Card Number",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreCustomer)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('corepos_account_id', model.CoreCustomer.corepos_account_id)
        g.set_filter('corepos_card_number', model.CoreCustomer.corepos_card_number)

    def configure_form(self, f):
        if not self.master.creating:
            f.append('corepos_account_id')
            f.append('corepos_card_number')

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreCustomer]

    def get_xref_buttons(self, customer):
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        url = corepos.get_office_member_url(customer.number)
        if url:
            return [{'url': url, 'text': "View in CORE Office"}]

    def get_xref_links(self, customer):
        if customer.corepos_card_number:
            url = self.request.route_url('corepos.members.view',
                                         card_number=customer.corepos_card_number)
            return [tags.link_to("View CORE-POS Member", url)]


class CustomerShopperViewSupplement(ViewSupplement):
    """
    CustomerShopper view supplement for CORE integration
    """
    route_prefix = 'customer_shoppers'

    labels = {
        'corepos_customer_id': "CORE-POS Customer ID",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreCustomerShopper)

    def configure_grid(self, g):
        model = self.model
        g.append('corepos_customer_id')
        g.set_filter('corepos_customer_id', model.CoreCustomerShopper.corepos_customer_id)
        g.set_sorter('corepos_customer_id', model.CoreCustomerShopper.corepos_customer_id)

    def configure_form(self, f):
        if not self.master.creating:
            f.append('corepos_customer_id')

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreCustomerShopper]


def includeme(config):
    CustomerViewSupplement.defaults(config)
    CustomerShopperViewSupplement.defaults(config)
