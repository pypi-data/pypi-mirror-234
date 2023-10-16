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
CORE-POS group views
"""

from collections import OrderedDict

from corepos.db.office_op import model as corepos

from webhelpers2.html import HTML

from .master import CoreOfficeMasterView


class UserGroupView(CoreOfficeMasterView):
    """
    Master view for CORE Office groups
    """
    model_class = corepos.UserGroup
    model_key = 'group_id'
    model_title = "CORE-POS User Group"
    url_prefix = '/core-pos/user-groups'
    route_prefix = 'corepos.user_groups'
    filterable = False
    pageable = False

    # TODO: maybe add support for these?
    creatable = False
    editable = False
    deletable = False

    labels = {
        'group_id': "Group ID",
    }

    grid_columns = [
        'group_id',
        'name',
    ]

    form_fields = [
        'group_id',
        'name',
        'users',
    ]

    def get_data(self, session=None):
        groups = OrderedDict()

        if session is None:
            session = self.Session()
        query = session.query(corepos.UserGroup)\
                       .order_by(corepos.UserGroup.group_id,
                                 corepos.UserGroup.name)

        for usergroup in query:
            if usergroup.group_id not in groups:
                groups[usergroup.group_id] = self.normalize(usergroup)

        return list(groups.values())

    def normalize(self, group):
        return {
            'group_id': group.group_id,
            'name': group.name,
        }

    def configure_grid(self, g):
        super(UserGroupView, self).configure_grid(g)

        g.sorters['group_id'] = g.make_simple_sorter('group_id')
        g.sorters['name'] = g.make_simple_sorter('name', foldcase=True)

        g.set_sort_defaults('group_id')

        g.set_link('group_id')
        g.set_link('name')

    def get_instance(self):
        gid = self.request.matchdict['group_id']
        group = self.Session.query(corepos.UserGroup)\
                            .filter(corepos.UserGroup.group_id == gid)\
                            .first()
        return self.normalize(group)

    def get_instance_title(self, group):
        return group['name']

    def configure_form(self, f):
        super(UserGroupView, self).configure_form(f)

        if self.creating or self.editing:
            f.remove('users')
        else:
            f.set_renderer('users', self.render_users)

    def render_users(self, group, field):
        groups = self.Session.query(corepos.UserGroup)\
                             .filter(corepos.UserGroup.group_id == group['group_id'])\
                             .order_by(corepos.UserGroup.username)\
                             .all()

        route_prefix = self.get_route_prefix()
        permission_prefix = self.get_permission_prefix()
        factory = self.get_grid_factory()
        g = factory(
            key='{}.users'.format(route_prefix),
            data=[],
            columns=[
                'username',
            ],
        )

        return HTML.literal(
            g.render_buefy_table_element(data_prop='usersData'))

    def template_kwargs_view(self, **kwargs):
        group_info = kwargs['instance']

        users_data = []
        usergroups = self.Session.query(corepos.UserGroup)\
                                 .filter(corepos.UserGroup.group_id == group_info['group_id'])\
                                 .order_by(corepos.UserGroup.username)
        for usergroup in usergroups:
            users_data.append({'username': usergroup.username})
        kwargs['users_data'] = users_data

        return kwargs


def defaults(config, **kwargs):
    base = globals()

    UserGroupView = kwargs.get('UserGroupView', base['UserGroupView'])
    UserGroupView.defaults(config)


def includeme(config):
    defaults(config)
