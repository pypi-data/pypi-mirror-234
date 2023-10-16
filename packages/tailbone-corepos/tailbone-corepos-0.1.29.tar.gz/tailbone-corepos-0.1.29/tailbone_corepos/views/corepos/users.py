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
CORE-POS user views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class UserView(CoreOfficeMasterView):
    """
    Master view for CORE Office Users
    """
    model_class = corepos.User
    model_key = 'name'
    model_title = "CORE-POS User"
    url_prefix = '/core-pos/users'
    route_prefix = 'corepos.users'

    labels = {
        'uid': "UID",
        'name': "Username",
        'session_id': "Session ID",
        'totp_url': "TOTP URL",
    }

    grid_columns = [
        'uid',
        'name',
        'real_name',
        'email',
    ]

    form_fields = [
        'uid',
        'name',
        'real_name',
        'email',
        'session_id',
        'totp_url',
    ]

    def configure_grid(self, g):
        super(UserView, self).configure_grid(g)

        if not hasattr(corepos.User, 'email'):
            g.remove('email')

        g.set_sort_defaults('name')

        g.set_link('uid')
        g.set_link('name')
        g.set_link('real_name')
        g.set_link('email')

    def configure_form(self, f):
        super(UserView, self).configure_form(f)

        if not hasattr(corepos.User, 'email'):
            f.remove('email')


def defaults(config, **kwargs):
    base = globals()

    UserView = kwargs.get('UserView', base['UserView'])
    UserView.defaults(config)


def includeme(config):
    defaults(config)
