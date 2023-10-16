## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.vendors.list'):
      <li>${h.link_to("View CORE-POS Vendors", url('corepos.vendors'))}</li>
  % endif
</%def>


${parent.body()}
