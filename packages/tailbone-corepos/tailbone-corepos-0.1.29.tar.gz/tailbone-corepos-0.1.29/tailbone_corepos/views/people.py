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
Person views
"""

from collections import OrderedDict

from tailbone.views import ViewSupplement


class PersonViewSupplement(ViewSupplement):
    """
    Person view supplement for CORE integration
    """
    route_prefix = 'people'

    labels = {
        'corepos_customer_id': "CORE-POS Customer ID",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.CorePerson)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('corepos_customer_id', model.CorePerson.corepos_customer_id)

    def configure_form(self, f):
        if not self.master.creating:
            f.append('corepos_customer_id')

    def get_version_child_classes(self):
        model = self.model
        return [model.CorePerson]

    def get_context_for_customer(self, customer, context):

        if customer.corepos_card_number:
            app = self.get_rattail_app()
            corepos = app.get_corepos_handler()
            url = corepos.get_office_member_url(customer.corepos_card_number)
            if url:
                context['external_links'].append({'label': "View in CORE Office",
                                                  'url': url})

        return context

    def get_member_xref_buttons(self, person):
        buttons = OrderedDict()
        app = self.get_rattail_app()
        corepos = app.get_corepos_handler()
        office_url = corepos.get_office_url()
        if office_url:
            kw = {'office_url': office_url}

            for member in person.members:
                url = corepos.get_office_member_url(member.number, **kw)
                buttons[member.uuid] = {'url': url, 'text': "View in CORE Office"}

            for customer in person.customers:
                for member in customer.members:
                    if member.uuid not in buttons:
                        url = corepos.get_office_member_url(member.number, **kw)
                        buttons[member.uuid] = {'url': url, 'text': "View in CORE Office"}

        return buttons.values()


def includeme(config):
    PersonViewSupplement.defaults(config)
