## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.products.list'):
      <li>${h.link_to("View CORE-POS Products", url('corepos.products'))}</li>
  % endif
</%def>


${parent.body()}
