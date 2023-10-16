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
CORE-POS "archive" transaction views
"""

from collections import OrderedDict

from corepos.db.office_arch.model import TransactionDetail

from .base import TransactionDetailMasterView
from tailbone_corepos.db import CoreTransArchiveSession, ExtraCoreTransArchiveSessions


class TransactionDetailView(TransactionDetailMasterView):
    """
    Master view for "archive" transaction details.
    """
    model_class = TransactionDetail
    model_title = "CORE-POS Archived Transaction Detail"
    url_prefix = '/corepos/transaction-details/archive'
    route_prefix = 'corepos.transaction_details_archive'

    @property
    def Session(self):
        """
        Which session we return will depend on user's "current" engine.
        """
        dbkey = self.get_current_engine_dbkey()

        if dbkey != 'default' and dbkey in ExtraCoreTransArchiveSessions:
            return ExtraCoreTransArchiveSessions[dbkey]

        return CoreTransArchiveSession

    def get_db_engines(self):
        engines = OrderedDict()
        if self.rattail_config.core_office_trans_archive_engine:
            engines['default'] = self.rattail_config.core_office_trans_archive_engine
        for dbkey in self.rattail_config.core_office_trans_archive_engines:
            if dbkey != 'default':
                engines[dbkey] = self.rattail_config.core_office_trans_archive_engines[dbkey]
        return engines

    def make_isolated_session(self):
        from corepos.db.office_trans import Session as CoreTransArchiveSession

        dbkey = self.get_current_engine_dbkey()
        if dbkey != 'default' and dbkey in self.rattail_config.core_office_trans_archive_engines:
            return CoreTransArchiveSession(bind=self.rattail_config.core_office_trans_archive_engines[dbkey])

        return CoreTransArchiveSession()


def defaults(config, **kwargs):
    base = globals()

    TransactionDetailView = kwargs.get('TransactionDetailView', base['TransactionDetailView'])
    TransactionDetailView.defaults(config)


def includeme(config):
    defaults(config)
