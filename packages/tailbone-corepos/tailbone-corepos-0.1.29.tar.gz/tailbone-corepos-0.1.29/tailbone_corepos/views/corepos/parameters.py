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
CORE POS parameter views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class ParameterView(CoreOfficeMasterView):
    """
    Master view for parameters
    """
    model_class = corepos.Parameter
    model_title = "CORE-POS Parameter"
    url_prefix = '/core-pos/parameters'
    route_prefix = 'corepos.parameters'
    creatable = True
    editable = True
    deletable = True

    labels = {
        'store_id': "Store ID",
        'lane_id': "Lane ID",
    }

    def configure_grid(self, g):
        super(ParameterView, self).configure_grid(g)

        g.set_link('param_key')
        g.set_link('param_value')


def defaults(config, **kwargs):
    base = globals()

    ParameterView = kwargs.get('ParameterView', base['ParameterView'])
    ParameterView.defaults(config)


def includeme(config):
    defaults(config)
