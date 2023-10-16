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
CORE-POS origin views
"""

from corepos.db.office_op import model as corepos

from deform import widget as dfwidget
from webhelpers2.html import tags

from .master import CoreOfficeMasterView


class OriginCountryView(CoreOfficeMasterView):
    """
    Master view for Origin Countries
    """
    model_class = corepos.OriginCountry
    model_title = "CORE-POS Origin Country"
    model_title_plural = "CORE-POS Origin Countries"
    url_prefix = '/core-pos/origins/countries'
    route_prefix = 'corepos.origin_countries'

    def configure_form(self, f):
        super(OriginCountryView, self).configure_form(f)

        if self.creating:
            f.remove('id')
        else:
            f.set_readonly('id')


class OriginStateProvinceView(CoreOfficeMasterView):
    """
    Master view for Origin State/Province
    """
    model_class = corepos.OriginStateProv
    model_title = "CORE-POS Origin State/Province"
    model_title_plural = "CORE-POS Origin States/Provinces"
    url_prefix = '/core-pos/origins/stateprov'
    route_prefix = 'corepos.origin_stateprov'

    def configure_form(self, f):
        super(OriginStateProvinceView, self).configure_form(f)

        if self.creating:
            f.remove('id')
        else:
            f.set_readonly('id')


class OriginRegionView(CoreOfficeMasterView):
    """
    Master view for Origin Custom Regions
    """
    model_class = corepos.OriginCustomRegion
    model_title = "CORE-POS Origin Region"
    url_prefix = '/core-pos/origins/regions'
    route_prefix = 'corepos.origin_regions'

    def configure_form(self, f):
        super(OriginRegionView, self).configure_form(f)

        if self.creating:
            f.remove('id')
        else:
            f.set_readonly('id')


class OriginView(CoreOfficeMasterView):
    """
    Base class for origin views.
    """
    model_class = corepos.Origin
    model_title = "CORE-POS Origin"
    url_prefix = '/core-pos/origins'
    route_prefix = 'corepos.origins'

    labels = {
        'country_id': "Country ID",
        'state_prov_id': "State/Province ID",
        'state_prov': "State/Province",
        'custom_id': "Custom Region ID",
    }

    grid_columns = [
        'id',
        'name',
        'short_name',
        'local',
        'country',
        'state_prov',
        'custom_region',
    ]

    form_fields = [
        'id',
        'name',
        'short_name',
        'local',
        'country',
        'state_prov',
        'custom_region',
    ]

    def configure_grid(self, g):
        super(OriginView, self).configure_grid(g)

        g.set_sort_defaults('id')
        g.set_link('name')
        g.set_link('short_name')

    def configure_form(self, f):
        super(OriginView, self).configure_form(f)

        # id
        if self.creating:
            f.remove('id')
        else:
            f.set_readonly('id')

        # country
        if self.creating or self.editing:
            f.replace('country', 'country_id')
            f.set_label('country_id', "Country")
            countries = self.Session.query(corepos.OriginCountry)\
                                    .order_by(corepos.OriginCountry.name)\
                                    .all()
            values = [(c.id, str(c)) for c in countries]
            f.set_widget('country_id', dfwidget.SelectWidget(values=values))
        else:
            f.set_renderer('country', self.render_country)

        # state_prov
        if self.creating or self.editing:
            f.replace('state_prov', 'state_prov_id')
            f.set_label('state_prov_id', "State/Province")
            stateprovs = self.Session.query(corepos.OriginStateProv)\
                                     .order_by(corepos.OriginStateProv.name)\
                                     .all()
            values = [(sp.id, str(sp)) for sp in stateprovs]
            f.set_widget('state_prov_id', dfwidget.SelectWidget(values=values))
        else:
            f.set_renderer('state_prov', self.render_stateprov)

        # custom_region
        if self.creating or self.editing:
            f.replace('custom_region', 'custom_id')
            f.set_label('custom_id', "Custom Region")
            regions = self.Session.query(corepos.OriginCustomRegion)\
                                  .order_by(corepos.OriginCustomRegion.name)\
                                  .all()
            values = [(r.id, str(r)) for r in regions]
            f.set_widget('custom_id', dfwidget.SelectWidget(values=values))
        else:
            f.set_renderer('custom_region', self.render_region)

    def render_country(self, origin, field):
        country = origin.country
        if country:
            text = str(country)
            if self.request.has_perm('corepos.origin_countries.view'):
                url = self.request.route_url('corepos.origin_countries.view', id=country.id)
                return tags.link_to(text, url)
            return text

    def render_stateprov(self, origin, field):
        state_prov = origin.state_prov
        if state_prov:
            text = str(state_prov)
            if self.request.has_perm('corepos.origin_stateprov.view'):
                url = self.request.route_url('corepos.origin_stateprov.view', id=state_prov.id)
                return tags.link_to(text, url)
            return text

    def render_region(self, origin, field):
        region = origin.custom_region
        if region:
            text = str(region)
            if self.request.has_perm('corepos.origin_regions.view'):
                url = self.request.route_url('corepos.origin_regions.view', id=region.id)
                return tags.link_to(text, url)
            return text


def defaults(config, **kwargs):
    base = globals()

    OriginCountryView = kwargs.get('OriginCountryView', base['OriginCountryView'])
    OriginCountryView.defaults(config)

    OriginStateProvinceView = kwargs.get('OriginStateProvinceView', base['OriginStateProvinceView'])
    OriginStateProvinceView.defaults(config)

    OriginRegionView = kwargs.get('OriginRegionView', base['OriginRegionView'])
    OriginRegionView.defaults(config)

    OriginView = kwargs.get('OriginView', base['OriginView'])
    OriginView.defaults(config)


def includeme(config):
    defaults(config)
