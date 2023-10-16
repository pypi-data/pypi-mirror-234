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
CORE-POS transaction views
"""

from collections import OrderedDict

from corepos.db.office_trans import model as coretrans

from rattail_corepos.corepos.office.importing.db.square import FromSquareToCoreTrans

from .base import TransactionDetailMasterView
from tailbone_corepos.db import CoreTransSession, ExtraCoreTransSessions


class TransactionDetailView(TransactionDetailMasterView):
    """
    Master view for "current" transaction details.
    """
    model_class = coretrans.TransactionDetail
    model_title = "CORE-POS Current Transaction Detail"
    url_prefix = '/corepos/transaction-details/current'
    route_prefix = 'corepos.transaction_details'
    bulk_deletable = True
    supports_import_batch_from_file = True

    @property
    def Session(self):
        """
        Which session we return will depend on user's "current" engine.
        """
        dbkey = self.get_current_engine_dbkey()

        if dbkey != 'default' and dbkey in ExtraCoreTransSessions:
            return ExtraCoreTransSessions[dbkey]

        return CoreTransSession

    def get_db_engines(self):
        engines = OrderedDict()
        if self.rattail_config.core_office_trans_engine:
            engines['default'] = self.rattail_config.core_office_trans_engine
        for dbkey in self.rattail_config.core_office_trans_engines:
            if dbkey != 'default':
                engines[dbkey] = self.rattail_config.core_office_trans_engines[dbkey]
        return engines

    def make_isolated_session(self):
        from corepos.db.office_trans import Session as CoreTransSession

        dbkey = self.get_current_engine_dbkey()
        if dbkey != 'default' and dbkey in self.rattail_config.core_office_trans_engines:
            return CoreTransSession(bind=self.rattail_config.core_office_trans_engines[dbkey])

        return CoreTransSession()

    def import_square(self):
        return self.import_batch_from_file(FromSquareToCoreTrans, 'TransactionDetail',
                                           importer_host_title="Square CSV")

    @classmethod
    def defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        permission_prefix = cls.get_permission_prefix()

        # import from square
        config.add_route('{}.import_square'.format(route_prefix), '{}/import-square'.format(url_prefix))
        config.add_view(cls, attr='import_square', route_name='{}.import_square'.format(route_prefix),
                        permission='{}.import_file'.format(permission_prefix))

        cls._defaults(config)


def defaults(config, **kwargs):
    base = globals()

    TransactionDetailView = kwargs.get('TransactionDetailView', base['TransactionDetailView'])
    TransactionDetailView.defaults(config)


def includeme(config):
    defaults(config)
