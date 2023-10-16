## -*- coding: utf-8; -*-
<%inherit file="/core-pos/master/view.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ${form.component_studly}Data.vendorItemsData = ${json.dumps(vendor_items_data)|n}

  </script>
</%def>

${parent.body()}
