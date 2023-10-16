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
CORE POS views
"""

from .master import CoreOfficeMasterView


def defaults(config, **kwargs):

    mod = lambda spec: kwargs.get(spec, spec)

    config.include(mod('tailbone_corepos.views.corepos.parameters'))
    config.include(mod('tailbone_corepos.views.corepos.tablesyncrules'))
    config.include(mod('tailbone_corepos.views.corepos.users'))
    config.include(mod('tailbone_corepos.views.corepos.groups'))
    config.include(mod('tailbone_corepos.views.corepos.stores'))
    config.include(mod('tailbone_corepos.views.corepos.departments'))
    config.include(mod('tailbone_corepos.views.corepos.subdepartments'))
    config.include(mod('tailbone_corepos.views.corepos.superdepartments'))
    config.include(mod('tailbone_corepos.views.corepos.vendors'))
    config.include(mod('tailbone_corepos.views.corepos.origins'))
    config.include(mod('tailbone_corepos.views.corepos.products'))
    config.include(mod('tailbone_corepos.views.corepos.likecodes'))
    config.include(mod('tailbone_corepos.views.corepos.scaleitems'))
    config.include(mod('tailbone_corepos.views.corepos.members'))
    config.include(mod('tailbone_corepos.views.corepos.customers'))
    config.include(mod('tailbone_corepos.views.corepos.employees'))
    config.include(mod('tailbone_corepos.views.corepos.coupons'))
    config.include(mod('tailbone_corepos.views.corepos.tenders'))
    config.include(mod('tailbone_corepos.views.corepos.stockpurchases'))
    config.include(mod('tailbone_corepos.views.corepos.taxrates'))
    config.include(mod('tailbone_corepos.views.corepos.transactions'))
    config.include(mod('tailbone_corepos.views.corepos.batches'))
    config.include(mod('tailbone_corepos.views.corepos.purchaseorders'))
    config.include(mod('tailbone_corepos.views.corepos.lanes'))


def includeme(config):
    defaults(config)
