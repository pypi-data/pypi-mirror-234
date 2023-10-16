## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.vendor_items.list'):
      <li>${h.link_to("View CORE-POS Vendor Items", url('corepos.vendor_items'))}</li>
  % endif
</%def>


${parent.body()}
