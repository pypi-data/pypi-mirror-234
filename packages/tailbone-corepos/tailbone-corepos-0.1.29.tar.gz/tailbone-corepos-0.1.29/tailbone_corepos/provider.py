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
Tailbone Provider for CORE-POS Integration
"""

from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import register

from tailbone.providers import TailboneProvider


class TailboneCorePosProvider(TailboneProvider):
    """
    View provider for tailbone-corepos
    """
    key = 'tailbone_corepos'

    def configure_db_sessions(self, rattail_config, pyramid_config):
        from tailbone_corepos.db import (CoreOfficeSession, 
                                         CoreTransSession,
                                         CoreTransArchiveSession,
                                         ExtraCoreOfficeSessions,
                                         ExtraCoreTransSessions,
                                         ExtraCoreTransArchiveSessions)

        # CORE-POS DB(s)
        CoreOfficeSession.configure(bind=rattail_config.core_office_op_engine)
        CoreTransSession.configure(bind=rattail_config.core_office_trans_engine)
        CoreTransArchiveSession.configure(
            bind=rattail_config.core_office_trans_archive_engine)

        # create session wrappers for each "extra" CORE DB engine
        for key, engine in rattail_config.core_office_op_engines.items():
            if key != 'default':
                Session = scoped_session(sessionmaker(bind=engine))
                register(Session)
                ExtraCoreOfficeSessions[key] = Session

        # create session wrappers for each "extra" CORE Transaction DB engine
        for key, engine in rattail_config.core_office_trans_engines.items():
            if key != 'default':
                Session = scoped_session(sessionmaker(bind=engine))
                register(Session)
                ExtraCoreTransSessions[key] = Session

        # and same for CORE Transaction Archive DB engine(s)
        for key, engine in rattail_config.core_office_trans_archive_engines.items():
            if key != 'default':
                Session = scoped_session(sessionmaker(bind=engine))
                register(Session)
                ExtraCoreTransArchiveSessions[key] = Session

    def get_provided_views(self):
        return {

            'corepos': {

                'people': {
                    'tailbone_corepos.views.corepos.customers': {
                        'label': "Customers",
                    },
                    'tailbone_corepos.views.corepos.employees': {
                        'label': "Employees",
                    },
                    'tailbone_corepos.views.corepos.groups': {
                        'label': "User Groups",
                    },
                    'tailbone_corepos.views.corepos.members': {
                        'label': "Members",
                    },
                    'tailbone_corepos.views.corepos.users': {
                        'label': "Users",
                    },
                },

                'products': {
                    'tailbone_corepos.views.corepos.departments': {
                        'label': "Departments",
                    },
                    'tailbone_corepos.views.corepos.subdepartments': {
                        'label': "Subdepartments",
                    },
                    'tailbone_corepos.views.corepos.superdepartments': {
                        'label': "Super Departments",
                    },
                    'tailbone_corepos.views.corepos.likecodes': {
                        'label': "Like Codes",
                    },
                    'tailbone_corepos.views.corepos.origins': {
                        'label': "Origins",
                    },
                    'tailbone_corepos.views.corepos.products': {
                        'label': "Products",
                    },
                    'tailbone_corepos.views.corepos.scaleitems': {
                        'label': "Scale Items",
                    },
                    'tailbone_corepos.views.corepos.vendoritems': {
                        'label': "Vendor Items",
                    },
                    'tailbone_corepos.views.corepos.vendors': {
                        'label': "Vendors",
                    },
                },

                'other': {
                    'tailbone_corepos.views.corepos.batches': {
                        'label': "Batches",
                    },
                    'tailbone_corepos.views.corepos.coupons': {
                        'label': "Coupons",
                    },
                    'tailbone_corepos.views.corepos.parameters': {
                        'label': "Parameters",
                    },
                    'tailbone_corepos.views.corepos.purchaseorders': {
                        'label': "Purchase Orders",
                    },
                    'tailbone_corepos.views.corepos.stores': {
                        'label': "Stores",
                    },
                    'tailbone_corepos.views.corepos.tablesyncrules': {
                        'label': "Table Sync Rules",
                    },
                    'tailbone_corepos.views.corepos.taxrates': {
                        'label': "Tax Rates",
                    },
                    'tailbone_corepos.views.corepos.transactions': {
                        'label': "Transactions",
                    },
                },
            },
        }

    def make_integration_menu(self, request, **kwargs):
        from tailbone_corepos.menus import make_corepos_menu
        return make_corepos_menu(request)
