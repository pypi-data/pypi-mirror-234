## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.origin_regions'):
      <li>${h.link_to("View CORE-POS Origin Regions", url('corepos.origin_regions'))}</li>
  % endif
  % if request.has_perm('corepos.origin_stateprov'):
      <li>${h.link_to("View CORE-POS Origin States/Provinces", url('corepos.origin_stateprov'))}</li>
  % endif
  % if request.has_perm('corepos.origin_countries'):
      <li>${h.link_to("View CORE-POS Origin Countries", url('corepos.origin_countries'))}</li>
  % endif
</%def>


${parent.body()}
