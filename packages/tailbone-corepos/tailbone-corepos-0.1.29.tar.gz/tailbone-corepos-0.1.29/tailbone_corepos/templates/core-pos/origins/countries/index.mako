## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.origins'):
      <li>${h.link_to("View CORE-POS Origins", url('corepos.origins'))}</li>
  % endif
</%def>


${parent.body()}
