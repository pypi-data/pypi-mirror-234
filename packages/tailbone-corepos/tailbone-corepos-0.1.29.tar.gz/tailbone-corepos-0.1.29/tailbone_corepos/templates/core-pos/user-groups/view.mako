## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ${form.component_studly}Data.usersData = ${json.dumps(users_data)|n}

  </script>
</%def>

${parent.body()}
