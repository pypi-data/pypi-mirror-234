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
CORE-POS tax rate views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class TaxRateView(CoreOfficeMasterView):
    """
    Master view for tax rates
    """
    model_class = corepos.TaxRate
    model_title = "CORE-POS Tax Rate"
    url_prefix = '/core-pos/tax-rates'
    route_prefix = 'corepos.taxrates'

    grid_columns = [
        'id',
        'rate',
        'description',
    ]

    form_fields = [
        'id',
        'rate',
        'description',
    ]

    def configure_grid(self, g):
        super(TaxRateView, self).configure_grid(g)

        g.set_link('id')
        g.set_link('description')


def defaults(config, **kwargs):
    base = globals()

    TaxRateView = kwargs.get('TaxRateView', base['TaxRateView'])
    TaxRateView.defaults(config)


def includeme(config):
    defaults(config)
