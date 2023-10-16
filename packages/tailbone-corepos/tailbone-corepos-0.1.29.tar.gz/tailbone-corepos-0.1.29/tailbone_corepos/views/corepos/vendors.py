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
CORE-POS vendor views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class VendorView(CoreOfficeMasterView):
    """
    Base class for vendor views.
    """
    model_class = corepos.Vendor
    model_key = 'id'
    model_title = "CORE-POS Vendor"
    url_prefix = '/core-pos/vendors'
    route_prefix = 'corepos.vendors'
    creatable = True
    editable = True
    deletable = True

    labels = {
        'id': "ID",
    }

    grid_columns = [
        'id',
        'name',
        'abbreviation',
        'discount_rate',
        'contact',
    ]

    form_fields = [
        'id',
        'name',
        'abbreviation',
        'discount_rate',
        'phone',
        'fax',
        'email',
        'website',
        'notes',
    ]

    has_rows = True
    model_row_class = corepos.VendorItem

    row_labels = {
        'vendor_item_id': "Vendor Item ID",
        'sku': "SKU",
        'upc': "UPC",
    }

    row_grid_columns = [
        'vendor_item_id',
        'sku',
        'upc',
        'brand',
        'description',
        'size',
        'cost',
        'units',
        'modified',
    ]

    def configure_grid(self, g):
        super(VendorView, self).configure_grid(g)

        # TODO: this is only needed b/c of orm.synonym usage
        g.set_sorter('id', corepos.Vendor.id)

        g.set_link('id')
        g.set_link('name')
        g.set_link('abbreviation')

    # TODO: ugh, would be nice to not have to do this...
    def get_action_route_kwargs(self, row):
        return {'id': row.id}

    def configure_form(self, f):
        super(VendorView, self).configure_form(f)

        if self.creating:
            f.remove_field('contact')

    def core_office_object_url(self, office_url, vendor):
        return '{}/item/vendors/VendorIndexPage.php?vid={}'.format(
            office_url, vendor.id)

    def get_row_data(self, vendor):
        return self.Session.query(corepos.VendorItem)\
                           .filter(corepos.VendorItem.vendor == vendor)

    def get_parent(self, item):
        return item.vendor

    def configure_row_grid(self, g):
        super(VendorView, self).configure_row_grid(g)

        g.set_type('units', 'quantity')
        g.set_sort_defaults('sku')

    def row_view_action_url(self, item, i):
        return self.request.route_url('corepos.vendor_items.view',
                                      **{'vendor_id': item.vendor.id,
                                         'sku': item.sku})


class VendorItemView(CoreOfficeMasterView):
    """
    Base class for vendor iem views.
    """
    model_class = corepos.VendorItem
    model_title = "CORE-POS Vendor Item"
    url_prefix = '/core-pos/vendor-items'
    route_prefix = 'corepos.vendor_items'

    labels = {
        'vendor_item_id': "ID",
        'sku': "SKU",
        'vendor_id': "Vendor ID",
        'upc': "UPC",
        'vendor_department_id': "Vendor Department ID",
        'srp': "SRP",
    }

    grid_columns = [
        'vendor_item_id',
        'sku',
        'vendor',
        'upc',
        'brand',
        'description',
        'size',
        'cost',
        'units',
        'modified',
    ]

    form_fields = [
        'vendor_item_id',
        'sku',
        'vendor_id',
        'vendor',
        'upc',
        'brand',
        'description',
        'size',
        'units',
        'cost',
        'sale_cost',
        'vendor_department_id',
        'srp',
        'modified',
    ]

    def configure_grid(self, g):
        super(VendorItemView, self).configure_grid(g)

        g.filters['upc'].default_active = True
        g.filters['upc'].default_verb = 'contains'

        g.set_type('units', 'quantity')

        g.set_sort_defaults('modified', 'desc')

        g.set_link('vendor_item_id')
        g.set_link('sku')
        g.set_link('vendor')
        g.set_link('upc')
        g.set_link('brand')
        g.set_link('description')

    def configure_form(self, f):
        super(VendorItemView, self).configure_form(f)

        f.set_type('units', 'quantity')
        f.set_type('srp', 'currency')

        f.set_readonly('vendor')

        if self.creating:
            f.remove('vendor_item_id')
        else:
            f.set_readonly('vendor_item_id')

        if self.creating or self.editing:
            f.remove('modified')
        else:
            f.set_readonly('modified')


def defaults(config, **kwargs):
    base = globals()

    VendorView = kwargs.get('VendorView', base['VendorView'])
    VendorView.defaults(config)

    VendorItemView = kwargs.get('VendorItemView', base['VendorItemView'])
    VendorItemView.defaults(config)


def includeme(config):
    defaults(config)
