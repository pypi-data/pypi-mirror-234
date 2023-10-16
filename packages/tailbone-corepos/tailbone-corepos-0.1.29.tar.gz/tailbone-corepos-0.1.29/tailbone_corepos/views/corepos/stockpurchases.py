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
Views for CORE-POS Stock Purchases
"""

from corepos.db.office_trans import model as corepos

from .master import CoreTransMasterView


class StockPurchaseView(CoreTransMasterView):
    """
    Master view for tax rates
    """
    model_class = corepos.StockPurchase
    model_title = "CORE-POS Stock Purchase"
    url_prefix = '/core-pos/stock-purchases'
    route_prefix = 'corepos.stock_purchases'
    supports_grid_totals = True

    labels = {
        'transaction_id': "Transaction ID",
    }

    def configure_grid(self, g):
        super().configure_grid(g)

        g.set_type('amount', 'currency')

        g.set_sort_defaults('datetime', 'desc')

        g.set_link('card_number')
        g.set_link('transaction_number')
        g.set_link('datetime')

    def fetch_grid_totals(self):
        app = self.get_rattail_app()
        results = self.get_effective_data()
        total = sum([purchase.amount for purchase in results])
        return {'totals_display': app.render_currency(total)}

    def configure_form(self, f):
        super().configure_form(f)

        f.set_renderer('card_number', self.render_linked_corepos_card_number)

        f.set_type('amount', 'currency')

        f.set_renderer('department_number',
                       self.render_linked_corepos_department_number)


def defaults(config, **kwargs):
    base = globals()

    StockPurchaseView = kwargs.get('StockPurchaseView', base['StockPurchaseView'])
    StockPurchaseView.defaults(config)


def includeme(config):
    defaults(config)
