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
CORE POS tender views
"""

from corepos.db.office_op.model import Tender

from .master import CoreOfficeMasterView


class TenderView(CoreOfficeMasterView):
    """
    Master view for tenders
    """
    model_class = Tender
    model_title = "CORE-POS Tender"
    url_prefix = '/core-pos/tenders'
    route_prefix = 'corepos.tenders'

    labels = {
        'tender_id': "Tender ID",
    }

    def configure_grid(self, g):
        super().configure_grid(g)

        g.set_link('tender_id')
        g.set_sort_defaults('tender_id')

        g.set_link('tender_name')

        g.set_type('min_amount', 'currency')
        g.set_type('max_amount', 'currency')
        g.set_type('max_refund', 'currency')


def defaults(config, **kwargs):
    base = globals()

    TenderView = kwargs.get('TenderView', base['TenderView'])
    TenderView.defaults(config)


def includeme(config):
    defaults(config)
