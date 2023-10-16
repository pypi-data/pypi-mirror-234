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
CORE-POS store views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class StoreView(CoreOfficeMasterView):
    """
    Base class for store views.
    """
    model_class = corepos.Store
    model_title = "CORE-POS Store"
    url_prefix = '/core-pos/stores'
    route_prefix = 'corepos.stores'

    labels = {
        'db_host': "DB Host",
        'db_driver': "DB Driver",
        'db_user': "DB User",
        'db_password': "DB Password",
        'trans_db': "Transactions DB",
        'op_db': "Operational DB",
        'web_service_url': "Web Service URL",
    }

    grid_columns = [
        'id',
        'description',
        'push',
        'pull',
        'has_own_items',
    ]

    form_fields = [
        'id',
        'description',
        'db_host',
        'db_driver',
        # TODO: should maybe expose these for admin only?
        # 'db_user',
        # 'db_password',
        'trans_db',
        'op_db',
        'push',
        'pull',
        'has_own_items',
        'web_service_url',
    ]

    def configure_grid(self, g):
        super(StoreView, self).configure_grid(g)

        # must add this b/c id is technically just a synonym
        g.set_sorter('id', corepos.Store.storeID)

        g.set_sort_defaults('id')

        g.set_link('id')
        g.set_link('description')


def defaults(config, **kwargs):
    base = globals()

    StoreView = kwargs.get('StoreView', base['StoreView'])
    StoreView.defaults(config)


def includeme(config):
    defaults(config)
