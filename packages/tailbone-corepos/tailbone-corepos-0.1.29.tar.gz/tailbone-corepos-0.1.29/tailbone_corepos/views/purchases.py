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
Purchase views
"""

import csv
import os

from tailbone.views.purchases import core as base


class PurchaseView(base.PurchaseView):
    """
    Expose some extra features per CORE-POS integration.
    """

    def template_kwargs_view(self, **kwargs):
        kwargs = super().template_kwargs_view(**kwargs)
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()

        url = corepos.get_office_url()
        if url:
            url = f'{url}/purchasing/ImportPurchaseOrder.php'
        kwargs['corepos_import_url'] = url

        return kwargs

    def download_for_corepos(self):
        """
        View for downloading a Purchase data file for import to CORE-POS.
        """
        purchase = self.get_instance()
        app = self.get_rattail_app()
        tmpdir = app.make_temp_dir()
        path = os.path.join(tmpdir, 'Purchase {}.csv'.format(purchase.id_str))

        fields = [
            'sku',
            'cost_total',
            'quantity_units',
            'quantity_cases',
            'units_per_case',
            'unit_size',
            'brand',
            'description',
            'upc_without_check',
            'upc_with_check',
        ]

        rows = []

        def collect(item, i):
            upc = item.upc
            if upc:
                # TODO: i am still confused by what really is expected for the
                # 'Unit Size' field here.  CORE *behavior* seems to prefer what
                # logically maps to Rattail `Product.unit_size` (e.g. 12) but
                # the data type for CORE `PurchaseOrderItems.unitSize` is varchar
                # and code comments imply e.g. '12 OZ' would also be expected.
                # for now i am being "conservative" and mimicking CORE *behavior*.
                unit_size = None
                if item.product:
                    unit_size = app.render_quantity(item.product.unit_size)
                rows.append({
                    'sku': item.vendor_code,
                    'cost_total': item.po_total,
                    'quantity_units': app.render_quantity(item.units_ordered),
                    'quantity_cases': app.render_quantity(item.cases_ordered),
                    'units_per_case': app.render_quantity(item.case_quantity),
                    'unit_size': unit_size,
                    'brand': item.brand_name,
                    'description': item.description,
                    'upc_without_check': str(upc)[:-1],
                    'upc_with_check': str(upc),
                })

        self.progress_loop(collect, purchase.items, None, # TODO
                           message="Converting data to CSV")

        with open(path, 'w') as f:
            writer = csv.DictWriter(f, fields)
            # note, the CORE importer does not really need or expect a header
            # TODO: seems like it should? b/c would be more helpful for humans
            #writer.writeheader()
            writer.writerows(rows)

        return self.file_response(path)

    @classmethod
    def defaults(cls, config):
        cls._corepos_purchase_defaults(config)
        cls._purchase_defaults(config)
        cls._defaults(config)

    @classmethod
    def _corepos_purchase_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        instance_url_prefix = cls.get_instance_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_title = cls.get_model_title()

        # download for core-pos
        config.add_route('{}.download_for_corepos'.format(route_prefix), '{}/download-for-corepos'.format(instance_url_prefix))
        config.add_view(cls, attr='download_for_corepos', route_name='{}.download_for_corepos'.format(route_prefix),
                        permission='{}.download_for_corepos'.format(permission_prefix))
        config.add_tailbone_permission(permission_prefix, '{}.download_for_corepos'.format(permission_prefix),
                                       "Download {} for import to CORE-POS".format(model_title))


def includeme(config):
    base.defaults(config, **{'PurchaseView': PurchaseView})
    config.include('tailbone.views.purchases.credits')
