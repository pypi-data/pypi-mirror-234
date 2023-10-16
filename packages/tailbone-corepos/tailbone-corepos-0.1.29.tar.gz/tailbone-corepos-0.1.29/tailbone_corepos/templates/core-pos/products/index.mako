## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.products_user.list'):
      <li>${h.link_to("View CORE-POS Products User", url('corepos.products_user'))}</li>
  % endif
</%def>


${parent.body()}
