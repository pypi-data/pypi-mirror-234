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
CORE-POS subdepartment views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class SubdepartmentView(CoreOfficeMasterView):
    """
    Base class for subdepartment views.
    """
    model_class = corepos.Subdepartment
    model_title = "CORE-POS Subdepartment"
    url_prefix = '/core-pos/subdepartments'
    route_prefix = 'corepos.subdepartments'

    grid_columns = [
        'number',
        'name',
        'department',
    ]

    def configure_grid(self, g):
        super(SubdepartmentView, self).configure_grid(g)

        g.filters['number'].default_active = True
        g.filters['number'].default_verb = 'equal'

        g.filters['name'].default_active = True
        g.filters['name'].default_verb = 'contains'

        g.set_sort_defaults('number')

        g.set_link('number')
        g.set_link('name')


def defaults(config, **kwargs):
    base = globals()

    SubdepartmentView = kwargs.get('SubdepartmentView', base['SubdepartmentView'])
    SubdepartmentView.defaults(config)


def includeme(config):
    defaults(config)
