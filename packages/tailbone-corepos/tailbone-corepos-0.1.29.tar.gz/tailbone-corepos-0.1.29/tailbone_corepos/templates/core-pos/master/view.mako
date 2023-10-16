## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />
<%namespace file="/corepos-util.mako" import="render_xref_helper" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ${render_xref_helper()}
</%def>


${parent.body()}
