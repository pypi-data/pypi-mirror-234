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
CORE-POS Like Code views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class LikeCodeView(CoreOfficeMasterView):
    """
    Base class for like code views.
    """
    model_class = corepos.LikeCode
    model_title = "CORE-POS Like Code"
    url_prefix = '/core-pos/like-codes'
    route_prefix = 'corepos.like_codes'
    results_downloadable = True

    has_rows = True
    model_row_class = corepos.Product

    labels = {
        'id': "Like Code",
        'preferred_vendor_id': "Preferred Vendor ID",
    }

    grid_columns = [
        'id',
        'description',
        'strict',
        'organic',
        'preferred_vendor_id',
        'multi_vendor',
        'sort_retail',
        'sort_internal',
    ]

    form_fields = [
        'id',
        'description',
        'strict',
        'organic',
        'preferred_vendor_id',
        'multi_vendor',
        'sort_retail',
        'sort_internal',
    ]

    row_labels = {
        'upc': "UPC",
    }

    row_grid_columns = [
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

    def configure_grid(self, g):
        super(LikeCodeView, self).configure_grid(g)

        g.remove_filter('likeCode')
        g.set_filter('id', corepos.LikeCode.id,
                     default_active=True,
                     default_verb='equal')

        g.sorters.pop('likeCode')
        g.set_sorter('id', corepos.LikeCode.id)
        g.set_sort_defaults('id')

        g.set_link('id')
        g.set_link('description')

    def get_row_data(self, likecode):
        return self.Session.query(corepos.Product)\
                           .join(corepos.ProductLikeCode)\
                           .filter(corepos.ProductLikeCode.like_code == likecode)

    def get_parent(self, product):
        return product._like_code.like_code

    def get_row_action_url(self, action, product, **kwargs):
        route_name = 'corepos.products.{}'.format(action)
        return self.request.route_url(route_name, id=product.id)

    def configure_row_grid(self, g):
        super(LikeCodeView, self).configure_row_grid(g)

        g.set_type('normal_price', 'currency')
        g.set_type('cost', 'currency')

        g.set_sort_defaults('upc')

        g.set_link('upc')
        g.set_link('description')


def defaults(config, **kwargs):
    base = globals()

    LikeCodeView = kwargs.get('LikeCodeView', base['LikeCodeView'])
    LikeCodeView.defaults(config)


def includeme(config):
    defaults(config)
