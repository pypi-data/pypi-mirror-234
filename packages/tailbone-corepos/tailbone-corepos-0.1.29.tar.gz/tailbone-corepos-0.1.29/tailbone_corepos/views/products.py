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
Product Views
"""

from webhelpers2.html import tags

from tailbone.views import ViewSupplement


class ProductViewSupplement(ViewSupplement):
    """
    Product view supplement for CORE integration
    """
    route_prefix = 'products'

    labels = {
        'corepos_id': "CORE-POS ID",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreProduct)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('corepos_id', model.CoreProduct.corepos_id)

    def configure_form(self, f):
        if not self.master.creating:
            f.append('corepos_id')

    # def objectify(self, form, data=None):
    #     if data is None:
    #         data = form.validated
    #     product = super(ProductView, self).objectify(form, data)
    #     return self.corepos_objectify(product)

    # def corepos_objectify(self, product):
    #     # remove the corepos extension record outright, if we just lost the ID
    #     if product._corepos and not product.corepos_id:
    #         self.Session.delete(product._corepos)
    #         self.Session.flush()
    #     return product

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreProduct]

    def get_panel_fields_main(self, product):
        return ['corepos_id']

    def get_xref_buttons(self, product):
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        url = corepos.get_office_product_url(product.item_id)
        if url:
            return [{'url': url, 'text': "View in CORE Office"}]

    def get_xref_links(self, product):
        if product.corepos_id:
            url = self.request.route_url('corepos.products.view',
                                         id=product.corepos_id)
            return [tags.link_to("View CORE-POS Product", url)]


def includeme(config):
    ProductViewSupplement.defaults(config)
