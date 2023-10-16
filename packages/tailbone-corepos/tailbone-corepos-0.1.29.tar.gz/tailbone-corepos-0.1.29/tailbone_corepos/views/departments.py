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
Department Views
"""

from tailbone.views import ViewSupplement


class DepartmentViewSupplement(ViewSupplement):
    """
    Department view supplement for CORE integration
    """
    route_prefix = 'departments'

    labels = {
        'corepos_number': "CORE-POS Number",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreDepartment)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('corepos_number', model.CoreDepartment.corepos_number)

    def configure_form(self, f):
        f.append('corepos_number')

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreDepartment]

    def get_xref_buttons(self, department):
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        url = corepos.get_office_url()
        if url:
            url = '{}/item/departments/DepartmentEditor.php?did={}'.format(
                url, department.number)
            return [{'url': url, 'text': "View in CORE Office"}]


def includeme(config):
    DepartmentViewSupplement.defaults(config)
