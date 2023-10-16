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
Web Views
"""


def includeme(config):

    # native view supplements
    config.include('tailbone_corepos.views.customers')
    config.include('tailbone_corepos.views.departments')
    config.include('tailbone_corepos.views.employees')
    config.include('tailbone_corepos.views.members')
    config.include('tailbone_corepos.views.people')
    config.include('tailbone_corepos.views.products')
    config.include('tailbone_corepos.views.stores')
    config.include('tailbone_corepos.views.subdepartments')
    config.include('tailbone_corepos.views.taxes')
    config.include('tailbone_corepos.views.tenders')
    config.include('tailbone_corepos.views.vendors')

    # CORE-POS tables
    config.include('tailbone_corepos.views.corepos')
