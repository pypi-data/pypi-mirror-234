## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('corepos.transaction_details_archive'):
      <li>${h.link_to("View Archive Details", url('corepos.transaction_details_archive'))}</li>
  % endif
</%def>

${parent.body()}
