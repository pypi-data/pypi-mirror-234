# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
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
CORE-POS transaction views (base)
"""

from tailbone_corepos.views.corepos.master import CoreMasterView


class TransactionDetailMasterView(CoreMasterView):
    """
    Master view for "current" transaction details.
    """
    labels = {
        'store_row_id': "Store Row ID",
        'store_id': "Store ID",
        'pos_row_id': "POS Row ID",
        'transaction_id': "Transaction ID",
        'upc': "UPC",
    }

    grid_columns = [
        'date_time',
        'register_number',
        'transaction_number',
        'card_number',
        'store_row_id',
        'upc',
        'description',
        'quantity',
        'unit_price',
        'discount',
        'total',
    ]

    def configure_grid(self, g):
        super(TransactionDetailMasterView, self).configure_grid(g)

        g.set_type('quantity', 'quantity')
        g.set_type('unit_price', 'currency')
        g.set_type('discount', 'currency')
        g.set_type('total', 'currency')

        g.set_sort_defaults('date_time', 'desc')

        g.set_label('register_number', "Register")
        g.set_label('transaction_number', "Trans. No.")
        g.set_label('card_number', "Card No.")
        g.set_label('department_number', "Dept. No.")

        g.set_link('upc')
        g.set_link('description')

    def configure_form(self, f):
        super(TransactionDetailMasterView, self).configure_form(f)

        f.set_type('quantity', 'quantity')
        f.set_type('unit_price', 'currency')
        f.set_type('discount', 'currency')
        f.set_type('total', 'currency')
