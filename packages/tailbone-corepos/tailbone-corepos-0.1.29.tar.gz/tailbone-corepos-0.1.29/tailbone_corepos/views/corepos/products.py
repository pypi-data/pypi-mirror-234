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
CORE-POS product views
"""

from corepos.db.office_op import model as corepos
from corepos.db.util import table_exists

from webhelpers2.html import HTML, tags

from .master import CoreOfficeMasterView


class ProductView(CoreOfficeMasterView):
    """
    Base class for product views.
    """
    model_class = corepos.Product
    model_title = "CORE-POS Product"
    url_prefix = '/core-pos/products'
    route_prefix = 'corepos.products'
    results_downloadable = True

    labels = {
        'id': "ID",
        'upc': "UPC",
        'department_number': "Dept. No.",
        'foodstamp': "Food Stamp",
        'unit_of_measure': "Unit of Measure",
        'quantity_enforced': "Qty. Enforced",
        'id_enforced': "ID Enforced",
        'subdepartment_number': "Subdept. No.",
        'default_vendor_id': "Default Vendor ID",
        'current_origin_id': "Current Origin ID",
        'tax_rate_id': "Tax Rate ID",
    }

    grid_columns = [
        'upc',
        'brand',
        'description',
        'size',
        'department',
        'vendor',
        'normal_price',
        'scale',
        'cost',
    ]

    form_fields = [
        'upc',
        'id',
        'brand',
        'description',
        'size',
        'unit_of_measure',
        'formatted_name',
        'tare_weight',

        'department_number',
        'department',
        'subdepartment_number',
        'subdepartment',

        'id_enforced',

        'in_use',
        'quantity_enforced',
        'scale',
        'scale_price',
        'food_stamp',
        'wicable',
        'line_item_discountable',
        'flags',

        'price_method',
        'group_price',
        'quantity',
        'special_price_method',
        'special_group_price',
        'special_quantity',
        'tax_rate_id',
        'tax_rate',
        'mix_match_code',
        'discount_type',

        'default_vendor_id',
        'default_vendor',
        'cost',
        'vendor_items',

        'normal_price',
        'special_price',
        'start_date',
        'end_date',

        'created',
        'modified',

        'discount',

        'deposit',
        'local',

        'store_id',
        'current_origin_id',
        'last_sold',

        'scale_item',
        'user_info',
        'physical_location',
        'like_code',
    ]

    def configure_grid(self, g):
        super(ProductView, self).configure_grid(g)

        g.set_joiner('department', lambda q: q.outerjoin(corepos.Department))
        g.set_sorter('department', corepos.Department.name)

        g.set_joiner('vendor', lambda q: q.outerjoin(corepos.Vendor,
                                                     corepos.Vendor.id == corepos.Product.default_vendor_id))
        g.set_sorter('vendor', corepos.Vendor.name)
        g.set_filter('vendor', corepos.Vendor.name)

        g.filters['upc'].default_active = True
        g.filters['upc'].default_verb = 'contains'

        g.filters['in_use'].default_active = True
        g.filters['in_use'].default_verb = 'is_true'

        g.set_type('cost', 'currency')
        g.set_type('normal_price', 'currency')

        g.set_sort_defaults('upc')

        g.set_link('upc')
        g.set_link('brand')
        g.set_link('description')

    def grid_extra_class(self, product, i):
        if not product.in_use:
            return 'warning'

    def get_instance_title(self, product):
        return "{} {}".format(product.upc, product.description)

    def configure_form(self, f):
        super(ProductView, self).configure_form(f)

        if not table_exists(self.Session(), corepos.FloorSection):
            f.remove('physical_location')

        f.set_renderer('vendor', self.render_corepos_vendor)

        f.set_renderer('vendor_items', self.render_vendor_items)

        f.set_renderer('flags', self.render_flags)
        f.set_renderer('user_info', self.render_user_info)

        # TODO: these fields are not yet editable; improve later as needed
        f.set_readonly('department')
        f.set_readonly('subdepartment')
        f.set_readonly('tax_rate')
        f.set_readonly('physical_location')
        f.set_readonly('default_vendor')
        f.set_readonly('start_date')
        f.set_readonly('end_date')
        f.set_readonly('created')
        f.set_readonly('modified')
        f.set_readonly('last_sold')
        if self.editing:
            f.remove('vendor_items')
            f.remove('scale_item')
            f.remove('user_info')

        f.set_type('start_date', 'datetime_local')
        f.set_type('end_date', 'datetime_local')
        f.set_type('last_sold', 'datetime_local')
        f.set_type('modified', 'datetime_local')

        f.set_type('normal_price', 'currency')
        f.set_type('group_price', 'currency')
        f.set_type('special_price', 'currency')
        f.set_type('special_group_price', 'currency')
        f.set_type('cost', 'currency')
        f.set_type('deposit', 'currency')

    def render_flags(self, product, field):
        flags = product.flags
        if not flags:
            return ""

        # fetch all flags which are actually defined (supported)
        supported = {}
        for flag in self.Session.query(corepos.ProductFlag):
            supported[flag.bit_number] = flag

        # convert product's flag value to string of bits
        bflags = bin(flags)[2:]   # remove '0b' prefix
        bflags = reversed(bflags) # make bit #1 first in string, etc.

        # create list of items to show each "set" flag
        items = []
        for i, bit in enumerate(bflags, 1):
            if bit == '1':
                flag = supported.get(i)
                if flag:
                    items.append(HTML.tag('li', c=flag.description))
                else:
                    items.append(HTML.tag('li', c="(unsupported bit #{})".format(i)))

        return HTML.tag('ul', c=items)

    def render_user_info(self, product, field):
        user_info = product.user_info
        if not user_info:
            return ""
        text = str(user_info)
        url = self.request.route_url('corepos.products_user.view', upc=user_info.upc)
        return tags.link_to(text, url)

    def render_vendor_items(self, product, field):
        route_prefix = self.get_route_prefix()
        permission_prefix = self.get_permission_prefix()

        factory = self.get_grid_factory()
        g = factory(
            key='{}.vendor_items'.format(route_prefix),
            data=[],
            columns=[
                'vendor_name',
                'sku',
                'size',
                'cost_display',
                'units',
            ],
            labels={
                'sku': "SKU",
                'vendor_name': "Vendor",
                'cost_display': "Cost",
            },
        )
        return HTML.literal(
            g.render_buefy_table_element(data_prop='vendorItemsData'))

    def template_kwargs_view(self, **kwargs):
        kwargs = super(ProductView, self).template_kwargs_view(**kwargs)
        product = kwargs['instance']
        app = self.get_rattail_app()

        vendor_items = []
        for item in product.vendor_items:
            vendor_items.append({
                'sku': item.sku,
                'vendor_name': item.vendor.name,
                'size': item.size,
                'cost_display': app.render_currency(item.cost),
                'units': item.units,
            })
        kwargs['vendor_items_data'] = vendor_items

        return kwargs

    def core_office_object_url(self, office_url, product):
        return '{}/item/ItemEditorPage.php?searchupc={}'.format(
            office_url, product.upc)

    def download_results_fields_available(self, **kwargs):
        fields = super(ProductView, self).download_results_fields_available(**kwargs)

        fields.append('superdepartment_number')

        return fields

    def download_results_setup(self, fields, progress=None):
        super(ProductView, self).download_results_setup(fields, progress=progress)

        if 'superdepartment_number' in fields:
            mapping = {}
            super_departments = self.Session.query(corepos.SuperDepartment).all()
            for superdept in super_departments:
                if superdept.child_id in mapping:
                    if superdept.parent_id < mapping[superdept.child_id]:
                        mapping[superdept.child_id] = superdept.parent_id
                else:
                    mapping[superdept.child_id] = superdept.parent_id
            self.supermap = mapping

    def download_results_normalize(self, product, fields, **kwargs):
        data = super(ProductView, self).download_results_normalize(product, fields, **kwargs)

        if 'superdepartment_number' in fields:
            data['superdepartment_number'] = None
            if product.department_number in self.supermap:
                data['superdepartment_number'] = self.supermap[product.department_number]

        return data


class ProductUserView(CoreOfficeMasterView):
    """
    Master view for `productUser` table
    """
    model_class = corepos.ProductUser
    model_title = "CORE-POS Product User"
    model_title_plural = "CORE-POS Products User"
    url_prefix = '/core-pos/products-user'
    route_prefix = 'corepos.products_user'

    labels = {
        'upc': "UPC",
    }

    grid_columns = [
        'upc',
        'description',
        'brand',
        'sizing',
        'enable_online',
        'sold_out',
    ]

    form_fields = [
        'upc',
        'product',
        'description',
        'brand',
        'sizing',
        'long_text',
        'photo',
        'enable_online',
        'sold_out',
        'sign_count',
    ]

    def configure_grid(self, g):
        super(ProductUserView, self).configure_grid(g)

        g.filters['upc'].default_active = True
        g.filters['upc'].default_verb = 'contains'

        g.set_sort_defaults('upc')

        g.set_link('upc')
        g.set_link('description')

    def configure_form(self, f):
        super(ProductUserView, self).configure_form(f)

        f.set_type('long_text', 'text')
        f.set_renderer('product', self.render_corepos_product)


class ProductFlagView(CoreOfficeMasterView):
    """
    Master view for product flags
    """
    model_class = corepos.ProductFlag
    model_title = "CORE-POS Product Flag"
    url_prefix = '/core-pos/product-flags'
    route_prefix = 'corepos.product_flags'

    def configure_grid(self, g):
        super(ProductFlagView, self).configure_grid(g)

        g.set_link('bit_number')
        g.set_link('description')

    def grid_extra_class(self, flag, i):
        if not flag.active:
            return 'warning'


def defaults(config, **kwargs):
    base = globals()

    ProductView = kwargs.get('ProductView', base['ProductView'])
    ProductView.defaults(config)

    ProductUserView = kwargs.get('ProductUserView', base['ProductUserView'])
    ProductUserView.defaults(config)

    ProductFlagView = kwargs.get('ProductFlagView', base['ProductFlagView'])
    ProductFlagView.defaults(config)


def includeme(config):
    defaults(config)
