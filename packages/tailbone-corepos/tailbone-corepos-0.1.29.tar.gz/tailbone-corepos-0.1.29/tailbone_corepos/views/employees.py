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
Employee Views
"""

from tailbone.views import ViewSupplement


class EmployeeViewSupplement(ViewSupplement):
    """
    Employee view supplement for CORE integration
    """
    route_prefix = 'employees'

    labels = {
        'corepos_number': "CORE-POS Number",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CoreEmployee)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('corepos_number', model.CoreEmployee.corepos_number)

    def configure_form(self, f):
        f.append('corepos_number')

    def get_version_child_classes(self):
        model = self.model
        return [model.CoreEmployee]

    def get_xref_buttons(self, employee):
        app = self.get_rattail_app()
        url = app.get_corepos_handler().get_office_employee_url(employee.corepos_number)
        if url:
            return [{'url': url, 'text': "View in CORE Office"}]


def includeme(config):
    EmployeeViewSupplement.defaults(config)
