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
CORE-POS department views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class DepartmentView(CoreOfficeMasterView):
    """
    Base class for department views.
    """
    model_class = corepos.Department
    model_title = "CORE-POS Department"
    url_prefix = '/core-pos/departments'
    route_prefix = 'corepos.departments'

    labels = {
        'see_id': "See ID",
        'modified_by_id': "Modified by ID",
    }

    grid_columns = [
        'number',
        'name',
        'tax',
        'food_stampable',
        'limit',
        'minimum',
        'discount',
        'see_id',
        'modified',
        'modified_by_id',
        'margin',
        'sales_code',
        'member_only',
    ]

    def configure_grid(self, g):
        super(DepartmentView, self).configure_grid(g)

        g.filters['number'].default_active = True
        g.filters['number'].default_verb = 'equal'

        g.filters['name'].default_active = True
        g.filters['name'].default_verb = 'contains'

        # TODO: it should be easier to set only grid header label
        g.set_label('food_stampable', "FS")
        g.filters['food_stampable'].label = "Food Stampable"

        g.set_type('modified', 'datetime_local')

        g.set_sort_defaults('number')

        g.set_link('number')
        g.set_link('name')

    def configure_form(self, f):
        super(DepartmentView, self).configure_form(f)
        f.set_type('modified', 'datetime_local')

    def core_office_object_url(self, office_url, department):
        return '{}/item/departments/DepartmentEditor.php?did={}'.format(
            office_url, department.number)


def defaults(config, **kwargs):
    base = globals()

    DepartmentView = kwargs.get('DepartmentView', base['DepartmentView'])
    DepartmentView.defaults(config)


def includeme(config):
    defaults(config)
