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
CORE POS batch views
"""

from corepos.db.office_op import model as corepos
from corepos import enum as corepos_enum

from .master import CoreOfficeMasterView


class BatchTypeView(CoreOfficeMasterView):
    """
    Master view for batch types
    """
    model_class = corepos.BatchType
    model_title = "CORE-POS Batch Type"
    url_prefix = '/core-pos/batch-types'
    route_prefix = 'corepos.batch_types'

    labels = {
        'editor_ui': "Editor UI",
    }

    def configure_grid(self, g):
        super(BatchTypeView, self).configure_grid(g)

        g.set_enum('discount_type', corepos_enum.BATCH_DISCOUNT_TYPE)

        g.set_sort_defaults('id')

        g.set_link('id')
        g.set_link('description')

    def configure_form(self, f):
        super(BatchTypeView, self).configure_form(f)

        f.set_enum('discount_type', corepos_enum.BATCH_DISCOUNT_TYPE)


class BatchView(CoreOfficeMasterView):
    """
    Master view for batches
    """
    model_class = corepos.Batch
    model_title = "CORE-POS Batch"
    model_title_plural = "CORE-POS Batches"
    url_prefix = '/core-pos/batches'
    route_prefix = 'corepos.batches'

    has_rows = True
    model_row_class = corepos.BatchItem
    rows_viewable = False
    rows_downloadable_xlsx = True

    grid_columns = [
        'id',
        'name',
        'batch_type',
        'item_count',
        'start_date',
        'end_date',
    ]

    form_fields = [
        'id',
        'name',
        'batch_type',
        'start_date',
        'end_date',
    ]

    row_labels = {
        'id': "ID",
        'batch_id': "Batch ID",
        'upc': "UPC",
    }

    row_grid_columns = [
        'id',
        'upc',
        'sale_price',
        'group_sale_price',
        'active',
        'price_method',
        'quantity',
        'sign_multiplier',
        'cost',
    ]

    def configure_grid(self, g):
        super(BatchView, self).configure_grid(g)

        g.set_renderer('start_date', self.render_local_date)
        g.set_renderer('end_date', self.render_local_date)

        g.set_renderer('item_count', self.render_item_count)

        g.set_sort_defaults('id', 'desc')

        g.set_link('id')
        g.set_link('name')

    def render_item_count(self, batch, field):
        return str(len(batch.items))

    def configure_form(self, f):
        super(BatchView, self).configure_form(f)

        f.set_type('start_date', 'datetime_local')
        f.set_type('end_date', 'datetime_local')

    def get_row_data(self, batch):
        return self.Session.query(corepos.BatchItem)\
                           .filter(corepos.BatchItem.batch == batch)

    def get_parent(self, item):
        return item.batch

    def configure_row_grid(self, g):
        super(BatchView, self).configure_row_grid(g)

        g.set_type('sale_price', 'currency')
        g.set_type('group_sale_price', 'currency')
        # TODO: some older installs don't have this field
        if hasattr(corepos.BatchItem, 'cost'):
            g.set_type('cost', 'currency')
        else:
            g.remove('cost')

        g.set_sort_defaults('id')


def defaults(config, **kwargs):
    base = globals()

    BatchTypeView = kwargs.get('BatchTypeView', base['BatchTypeView'])
    BatchTypeView.defaults(config)

    BatchView = kwargs.get('BatchView', base['BatchView'])
    BatchView.defaults(config)


def includeme(config):
    defaults(config)
