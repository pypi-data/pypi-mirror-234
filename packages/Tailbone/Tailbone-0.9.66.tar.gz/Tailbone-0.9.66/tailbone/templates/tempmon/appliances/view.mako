## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('tempmon.appliances.dashboard'):
      <li>${h.link_to("Go to the Dashboard", url('tempmon.dashboard'))}</li>
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ${form.component_studly}Data.probesData = ${json.dumps(probes_data)|n}

  </script>
</%def>


${parent.body()}
