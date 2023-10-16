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
CORE POS purchase order views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class PurchaseOrderView(CoreOfficeMasterView):
    """
    Master view for purchase orders
    """
    model_class = corepos.PurchaseOrder
    model_title = "CORE-POS Purchase Order"
    url_prefix = '/core-pos/purchase-orders'
    route_prefix = 'corepos.purchase_orders'

    has_rows = True
    model_row_class = corepos.PurchaseOrderItem
    rows_viewable = False
    rows_downloadable_xlsx = True

    labels = {
        'vendor_id': "Vendor ID",
        'store_id': "Store ID",
        'user_id': "User ID",
        'vendor_order_id': "Vendor Order ID",
        'vendor_invoice_id': "Vendor Invoice ID",
        'standing_id': "Standing ID",
        'transfer_id': "Transfer ID",
    }

    grid_columns = [
        'id',
        'vendor',
        'store_id',
        'creation_date',
        'placed',
        'placed_date',
        'vendor_order_id',
        'vendor_invoice_id',
    ]

    form_fields = [
        'id',
        'vendor_id',
        'vendor',
        'store_id',
        'store',
        'creation_date',
        'placed',
        'placed_date',
        'user_id',
        'vendor_order_id',
        'vendor_invoice_id',
        'standing_id',
        'inventory_ignore',
        'transfer_id',
        'notes',
    ]

    row_labels = {
        'sku': "SKU",
        'internal_upc': "Internal UPC",
        'is_special_order': "Special Order",
    }

    row_grid_columns = [
        'sku',
        'internal_upc',
        'brand',
        'description',
        'unit_size',
        'unit_cost',
        'case_size',
        'quantity',
        'received_date',
        'received_quantity',
        'received_total_cost',
        'is_special_order',
    ]

    def configure_grid(self, g):
        super(PurchaseOrderView, self).configure_grid(g)

        g.set_joiner('vendor', lambda q: q.outerjoin(
            corepos.Vendor,
            corepos.Vendor.id == corepos.PurchaseOrder.vendor_id))
        g.set_sorter('vendor', corepos.Vendor.name)
        g.set_filter('vendor', corepos.Vendor.name)

        # g.set_joiner('store', lambda q: q.outerjoin(
        #     corepos.Store,
        #     corepos.Store.id == corepos.PurchaseOrder.store_id))
        # g.set_sorter('store', corepos.Store.description)

        g.set_sorter('id', corepos.PurchaseOrder.id)
        g.set_sort_defaults('id', 'desc')

        g.set_link('id')
        g.set_link('vendor')

    def configure_form(self, f):
        super(PurchaseOrderView, self).configure_form(f)

        f.set_renderer('vendor', self.render_corepos_vendor)

        f.set_renderer('store', self.render_corepos_store)

        f.set_type('notes', 'text')

    def core_office_object_url(self, office_url, order):
        return '{}/purchasing/ViewPurchaseOrders.php?id={}'.format(
            office_url, order.id)

    def get_row_data(self, order):
        return self.Session.query(corepos.PurchaseOrderItem)\
                           .filter(corepos.PurchaseOrderItem.order == order)

    def get_parent(self, item):
        return item.order

    def configure_row_grid(self, g):
        super(PurchaseOrderView, self).configure_row_grid(g)

        g.set_label('received_quantity', "Received Qty.")
        g.filters['received_quantity'].label = "Received Quantity"

        g.set_label('received_total_cost', "Received Cost")
        g.filters['received_total_cost'].label = "Received Total Cost"

        g.set_type('unit_cost', 'currency')
        g.set_type('case_size', 'quantity')
        g.set_type('quantity', 'quantity')
        g.set_type('received_quantity', 'quantity')
        g.set_type('received_total_cost', 'currency')


def defaults(config, **kwargs):
    base = globals()

    PurchaseOrderView = kwargs.get('PurchaseOrderView', base['PurchaseOrderView'])
    PurchaseOrderView.defaults(config)


def includeme(config):
    defaults(config)
