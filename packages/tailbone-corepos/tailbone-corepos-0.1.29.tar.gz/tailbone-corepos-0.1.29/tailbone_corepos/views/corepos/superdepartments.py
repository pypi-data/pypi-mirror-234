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
CORE-POS supersuperdepartment views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView
from . import departments as base


class SuperDepartmentView(base.DepartmentView):
    """
    Base class for super department views.  Which is really just a particular
    kind of view for certain "departments".
    """
    model_title = "CORE-POS Super Department"
    url_prefix = '/core-pos/super-departments'
    route_prefix = 'corepos.super_departments'
    creatable = False
    deletable = False

    has_rows = True
    model_row_class = corepos.Department
    rows_viewable = False

    grid_columns = [
        'number',
        'name',
        'members',
    ]

    form_fields = [
        'number',
        'name',
    ]

    row_labels = {
        'see_id': "See ID",
        'modified_by_id': "Modified by ID",
    }

    row_grid_columns = [
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

    def query(self, session):

        # find the distinct set of parent (super) department numbers
        query = session.query(corepos.SuperDepartment.parent_id).distinct()
        parent_numbers = [row[0] for row in query]

        # build the base/default Department query
        query = super(SuperDepartmentView, self).query(session)

        # if we actually have super departments, then we filter the query
        if parent_numbers:
            query = query.filter(corepos.Department.number.in_(parent_numbers))
        else: # otherwise we ensure query has no results
            query = query.filter(corepos.Department.number == None)

        return query

    def configure_grid(self, g):
        super(SuperDepartmentView, self).configure_grid(g)

        g.set_renderer('members', self.render_members)

        g.set_sort_defaults('name')

    def configure_form(self, f):
        super(SuperDepartmentView, self).configure_form(f)

        f.set_readonly('number')

    def render_members(self, department, field):
        return str(len(department._super_children))

    def get_row_data(self, parent):

        # find all "child" department numbers
        query = self.Session().query(corepos.SuperDepartment)\
                              .filter(corepos.SuperDepartment.parent == parent)
        child_numbers = [superdept.child_id for superdept in query]

        # return a query on Department with only those child numbers
        query = self.Session().query(corepos.Department)
        if child_numbers:
            query = query.filter(corepos.Department.number.in_(child_numbers))
        else:
            query = query.filter(corepos.Department.number == None)
        return query

    def get_parent(self, child):
        return child._super_parents[0].parent

    def configure_row_grid(self, g):
        super(SuperDepartmentView, self).configure_row_grid(g)

        g.set_type('modified', 'datetime_local')

        g.set_sort_defaults('number')


def defaults(config, **kwargs):
    base = globals()

    SuperDepartmentView = kwargs.get('SuperDepartmentView', base['SuperDepartmentView'])
    SuperDepartmentView.defaults(config)


def includeme(config):
    defaults(config)
