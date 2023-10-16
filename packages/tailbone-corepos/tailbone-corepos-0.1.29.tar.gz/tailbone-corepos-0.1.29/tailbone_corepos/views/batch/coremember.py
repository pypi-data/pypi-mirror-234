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
Views for CORE member batches
"""

from corepos.db.office_op import model as corepos

from rattail_corepos.db.model import CoreMemberBatch, CoreMemberBatchRow
from rattail_corepos.batch.coremember import CoreMemberBatchHandler

from tailbone.views.batch import BatchMasterView
from tailbone_corepos.db import CoreOfficeSession


class CoreMemberBatchView(BatchMasterView):
    """
    Master view for CORE member batches.
    """
    model_class = CoreMemberBatch
    model_row_class = CoreMemberBatchRow
    batch_handler_class = CoreMemberBatchHandler
    route_prefix = 'batch.coremember'
    url_prefix = '/batch/corepos-member'
    downloadable = True
    rows_bulk_deletable = True

    grid_columns = [
        'id',
        'description',
        'input_file',
        'created',
        'created_by',
        'rowcount',
        'executed',
        'executed_by',
    ]

    form_fields = [
        'id',
        'input_file',
        'description',
        'notes',
        'params',
        'created',
        'created_by',
        'rowcount',
        'executed',
        'executed_by',
    ]

    row_labels = {
        'email1': "Email",
        'member_type_id': "Member Type",
    }

    row_grid_columns = [
        'sequence',
        'card_number',
        'first_name',
        'last_name',
        'email1',
        'phone',
        'member_type_id',
        'status_code',
    ]

    row_form_fields = [
        'sequence',
        'card_number',
        'card_number_raw',
        'status_code',
        'status_text',
    ]

    def configure_grid(self, g):
        super(CoreMemberBatchView, self).configure_grid(g)

        g.set_link('input_file')

    def configure_form(self, f):
        super(CoreMemberBatchView, self).configure_form(f)

        # input_file
        if self.creating:
            f.set_type('input_file', 'file')
        else:
            f.set_readonly('input_file')
            f.set_renderer('input_file', self.render_downloadable_file)

    def configure_row_grid(self, g):
        super(CoreMemberBatchView, self).configure_row_grid(g)

        app = self.get_rattail_app()
        member_types = app.cache_model(CoreOfficeSession(),
                                       corepos.MemberType,
                                       normalizer=lambda mtype: mtype.description,
                                       key=lambda mtype, normal: mtype.id)
        g.set_enum('member_type_id', member_types)

        g.set_link('card_number')
        g.set_link('first_name')
        g.set_link('last_name')
        g.set_link('email1')

    def row_grid_extra_class(self, row, i):
        if row.status_code == row.STATUS_MEMBER_NOT_FOUND:
            return 'warning'
        if row.status_code in (row.STATUS_FIELDS_CHANGED,):
            return 'notice'

    def template_kwargs_view_row(self, **kwargs):
        app = self.get_rattail_app()
        batch = kwargs['parent_instance']
        row = kwargs['instance']
        kwargs['batch'] = batch
        kwargs['instance_title'] = batch.id_str

        fields = batch.get_param('fields')

        kwargs['diff_fields'] = fields
        kwargs['diff_old_values'] = dict([
            (field, getattr(row, '{}_old'.format(field)))
            for field in fields])
        kwargs['diff_new_values'] = dict([
            (field, getattr(row, field))
            for field in fields])

        # CORE Office URL
        kwargs['core_office_url'] = None
        if row.card_number:
            corepos = app.get_corepos_handler()
            office_url = corepos.get_office_url()
            if not office_url:
                kwargs['core_office_why_no_url'] = "CORE Office URL is not configured"
            else:
                url = corepos.get_office_member_url(row.card_number, office_url=office_url)
                if url:
                    kwargs['core_office_url'] = url
                else:
                    kwargs['core_office_why_no_url'] = "URL not defined for this object"

        else:
            kwargs['core_office_why_no_url'] = "Card number not valid"

        return kwargs


def includeme(config):
    CoreMemberBatchView.defaults(config)
