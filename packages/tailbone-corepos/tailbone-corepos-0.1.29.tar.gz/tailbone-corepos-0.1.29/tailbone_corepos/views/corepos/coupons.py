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
CORE POS coupon views
"""

from corepos.db.office_op import model as corepos
from corepos import enum as corepos_enum

from .master import CoreOfficeMasterView


class HouseCouponView(CoreOfficeMasterView):
    """
    Master view for house (store) coupons
    """
    model_class = corepos.HouseCoupon
    model_title = "CORE-POS House Coupon"
    url_prefix = '/core-pos/house-coupons'
    route_prefix = 'corepos.house_coupons'
    editable = True

    labels = {
        'coupon_id': "Coupon ID",
        'department_id': "Department Number", # filter
    }

    grid_columns = [
        'coupon_id',
        'description',
        'department',
        'discount_type',
        'discount_value',
        'start_date',
        'end_date',
    ]

    form_fields = [
        'coupon_id',
        'description',
        'limit',
        'start_date',
        'end_date',
        'member_only',
        'auto',
        'department',
        'min_type',
        'min_value',
        'discount_type',
        'discount_value',
        'virtual_only',
    ]

    def configure_grid(self, g):
        super(HouseCouponView, self).configure_grid(g)

        g.set_enum('discount_type', corepos_enum.HOUSE_COUPON_DISCOUNT_TYPE)

        g.set_renderer('start_date', self.render_local_date)
        g.set_renderer('end_date', self.render_local_date)

        g.set_joiner('department', lambda q: q.outerjoin(corepos.Department))
        g.set_filter('department', corepos.Department.name, label="Department Name")
        g.set_sorter('department', corepos.Department.name)

        g.set_sort_defaults('coupon_id', 'desc')

        g.set_link('coupon_id')
        g.set_link('description')

    def configure_form(self, f):
        super(HouseCouponView, self).configure_form(f)

        if self.creating:
            f.remove('coupon_id')
        else:
            f.set_readonly('coupon_id')

        f.set_enum('member_only', corepos_enum.HOUSE_COUPON_MEMBER_ONLY)

        f.set_renderer('department', self.render_corepos_department)

        f.set_enum('discount_type', corepos_enum.HOUSE_COUPON_DISCOUNT_TYPE)

        f.set_enum('min_type', corepos_enum.HOUSE_COUPON_MINIMUM_TYPE)

        f.set_readonly('department') # TODO: show dropdown for this

        f.set_renderer('start_date', self.render_local_date)
        f.set_readonly('start_date') # TODO
        f.set_type('start_date', 'date_jquery')

        f.set_renderer('end_date', self.render_local_date)
        f.set_readonly('end_date') # TODO
        f.set_type('end_date', 'date_jquery')


def defaults(config, **kwargs):
    base = globals()

    HouseCouponView = kwargs.get('HouseCouponView', base['HouseCouponView'])
    HouseCouponView.defaults(config)


def includeme(config):
    defaults(config)
