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
Views for CORE equity import batches
"""

from corepos.db.office_op import model as corepos

from rattail_corepos.db.model import CoreEquityImportBatch, CoreEquityImportBatchRow
from rattail_corepos.batch.equityimport import CoreEquityImportBatchHandler

from webhelpers2.html import tags

from tailbone.views.batch import BatchMasterView
from tailbone_corepos.db import CoreOfficeSession


class CoreEquityImportBatchView(BatchMasterView):
    """
    Master view for CORE member batches.
    """
    model_class = CoreEquityImportBatch
    model_row_class = CoreEquityImportBatchRow
    batch_handler_class = CoreEquityImportBatchHandler
    route_prefix = 'batch.corepos.equity_import'
    url_prefix = '/batch/corepos-equity-import'
    rows_bulk_deletable = True

    row_labels = {
        'member_type_id': "Member Type",
        'corepos_equity_total': "CORE-POS Equity Total",
    }

    row_grid_columns = [
        'sequence',
        'card_number',
        'first_name',
        'last_name',
        'member_type_id',
        'payment_amount',
        'department_number',
        'tender_code',
        'timestamp',
        'status_code',
    ]

    row_form_fields = [
        'sequence',
        'payment',
        'card_number',
        'first_name',
        'last_name',
        'member_type_id',
        'payment_amount',
        'department_number',
        'tender_code',
        'timestamp',
        'corepos_equity_total',
        'rattail_equity_total',
        'other_equity_total',
        'status_code',
    ]

    def configure_row_grid(self, g):
        super().configure_row_grid(g)
        app = self.get_rattail_app()
        model = self.model

        # card_number
        g.set_link('card_number')
        if 'card_number' in g.filters:
            g.filters['card_number'].default_active = True
            g.filters['card_number'].default_verb = 'equal'

        # *_name
        g.set_link('first_name')
        g.set_link('last_name')

        # member_type_id
        query = self.Session.query(model.MembershipType)\
                            .order_by(model.MembershipType.name)
        memtypes = app.cache_model(self.Session(), model.MembershipType, query=query,
                                   key='number', normalizer=lambda t: str(t))
        g.set_enum('member_type_id', memtypes)

        # payment_amount
        g.set_type('payment_amount', 'currency')

        # department_number
        g.set_label('department_number', "Department")
        if 'department_number' in g.filters:
            g.filters['department_number'].label = "Department Number"

    def row_grid_extra_class(self, row, i):
        if row.status_code in (row.STATUS_MEMBER_NOT_FOUND,
                               row.STATUS_MISSING_VALUES,
                               row.STATUS_ALREADY_IN_CORE):
            return 'warning'
        if row.status_code in (row.STATUS_NEEDS_ATTENTION,
                               row.STATUS_EQUITY_OVERPAID):
            return 'notice'

    def configure_row_form(self, f):
        super().configure_row_form(f)
        app = self.get_rattail_app()
        model = self.model

        f.set_renderer('payment', self.render_payment)

        query = self.Session.query(model.MembershipType)\
                            .order_by(model.MembershipType.name)
        memtypes = app.cache_model(self.Session(), model.MembershipType, query=query,
                                   key='number', normalizer=lambda t: str(t))
        f.set_enum('member_type_id', memtypes)

        f.set_type('payment_amount', 'currency')
        f.set_type('corepos_equity_total', 'currency')
        f.set_type('rattail_equity_total', 'currency')
        f.set_type('other_equity_total', 'currency')

    def render_payment(self, row, field):
        payment = getattr(row, field)
        if not payment:
            return

        text = str(payment)
        url = self.request.route_url('member_equity_payments.view', uuid=payment.uuid)
        return tags.link_to(text, url)


def includeme(config):
    CoreEquityImportBatchView.defaults(config)
