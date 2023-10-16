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
CORE-POS TableSyncRule views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class TableSyncRuleView(CoreOfficeMasterView):
    """
    Master view for table sync rules
    """
    model_class = corepos.TableSyncRule
    model_title = "CORE-POS Table Sync Rule"
    url_prefix = '/core-pos/table-sync-rules'
    route_prefix = 'corepos.table_sync_rules'


def defaults(config, **kwargs):
    base = globals()

    TableSyncRuleView = kwargs.get('TableSyncRuleView', base['TableSyncRuleView'])
    TableSyncRuleView.defaults(config)


def includeme(config):
    defaults(config)
