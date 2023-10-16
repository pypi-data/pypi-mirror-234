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
CORE-POS scale item views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class ScaleItemView(CoreOfficeMasterView):
    """
    Base class for scale item views.
    """
    model_class = corepos.ScaleItem
    model_title = "CORE-POS Scale Item"
    url_prefix = '/core-pos/scale-items'
    route_prefix = 'corepos.scale_items'
    results_downloadable = True

    labels = {
        'plu': "PLU",
    }

    grid_columns = [
        'plu',
        'product',
        'price',
        'origin_text',
        'modified',
    ]

    def configure_grid(self, g):
        super(ScaleItemView, self).configure_grid(g)

        g.filters['plu'].default_active = True
        g.filters['plu'].default_verb = 'contains'

        g.set_type('price', 'currency')

        g.set_sort_defaults('plu')

        g.set_link('plu')
        g.set_link('product')

    def configure_form(self, f):
        super(ScaleItemView, self).configure_form(f)

        f.set_renderer('product', self.render_corepos_product)


def defaults(config, **kwargs):
    base = globals()

    ScaleItemView = kwargs.get('ScaleItemView', base['ScaleItemView'])
    ScaleItemView.defaults(config)


def includeme(config):
    defaults(config)
