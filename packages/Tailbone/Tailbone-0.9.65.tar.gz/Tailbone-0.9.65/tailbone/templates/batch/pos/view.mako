## -*- coding: utf-8; -*-
<%inherit file="/batch/view.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ${form.component_studly}Data.taxesData = ${json.dumps(taxes_data)|n}

  </script>
</%def>

${parent.body()}
