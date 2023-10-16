## -*- coding: utf-8; -*-

<%def name="render_xref_button()">
  <b-button type="is-primary"
            % if core_office_url:
            tag="a" href="${core_office_url}" target="_blank"
            % else:
            disabled title="${core_office_why_no_url}"
            % endif
            icon-pack="fas"
            icon-left="fas fa-external-link-alt">
    View in CORE Office
  </b-button>
</%def>

<%def name="render_xref_helper()">
  <div class="object-helper">
    <h3>Cross-Reference</h3>
    <div class="object-helper-content">
      ${self.render_xref_button()}
    </div>
  </div>
</%def>
