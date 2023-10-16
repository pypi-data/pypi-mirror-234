## -*- coding: utf-8; -*-
<%inherit file="/master/view_row.mako" />
<%namespace file="/corepos-util.mako" import="render_xref_helper" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ${render_xref_helper()}
</%def>

<%def name="field_diff_table()">
  <table class="diff monospace dirty">
    <thead>
      <tr>
        <th>field name</th>
        <th>old value</th>
        <th>new value</th>
      </tr>
    </thead>
    <tbody>
      % for field in diff_fields:
         <tr${' class="diff"' if diff_new_values[field] != diff_old_values[field] else ''|n}>
           <td class="field">${field}</td>
           <td class="value old-value">${repr(diff_old_values[field])}</td>
           <td class="value new-value">${repr(diff_new_values[field])}</td>
         </tr>
      % endfor
    </tbody>
  </table>
</%def>

<%def name="render_buefy_form()">
  <div class="form">
    <tailbone-form></tailbone-form>
    <br />
    ${self.field_diff_table()}
  </div>
</%def>


${parent.body()}
