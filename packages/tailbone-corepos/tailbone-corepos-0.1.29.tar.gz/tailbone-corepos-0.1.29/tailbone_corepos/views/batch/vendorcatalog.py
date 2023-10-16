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
Vendor Catalog batch views for CORE-POS
"""

from corepos.db.office_op import model as corepos

from deform import widget as dfwidget

from tailbone.views.batch import vendorcatalog as base
from tailbone_corepos.db import CoreOfficeSession


class VendorCatalogView(base.VendorCatalogView):
    """
    Master view for vendor catalog batches.
    """

    def configure_form(self, f):
        super(VendorCatalogView, self).configure_form(f)
        model = self.model

        # replace stock 'vendor' field with id/name combo
        f.remove('vendor', 'vendor_uuid')
        f.insert_after('parser_key', 'vendor_id')
        f.insert_after('vendor_id', 'vendor_name')

        # vendor_id
        if self.creating:
            vendors = CoreOfficeSession.query(corepos.Vendor)\
                                       .order_by(corepos.Vendor.name)\
                                       .all()
            values = [(str(vendor.id), vendor.name)
                      for vendor in vendors]
            f.set_widget('vendor_id', dfwidget.SelectWidget(values=values))
            f.set_required('vendor_id')
            f.set_label('vendor_id', "Vendor")

        # vendor_name
        if self.creating:
            f.remove('vendor_name')

    def get_batch_kwargs(self, batch):
        kwargs = super(VendorCatalogView, self).get_batch_kwargs(batch)

        if 'vendor_name' not in kwargs and batch.vendor_id:
            vendor = CoreOfficeSession.get(corepos.Vendor, batch.vendor_id)
            if vendor:
                kwargs['vendor_name'] = vendor.name

        return kwargs


def defaults(config, **kwargs):
    kwargs.setdefault('VendorCatalogView', VendorCatalogView)
    base.defaults(config, **kwargs)


def includeme(config):
    defaults(config)
