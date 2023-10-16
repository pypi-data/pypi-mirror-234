## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="object_helpers()"></%def>

<%def name="render_form_buttons()"></%def>

<%def name="render_form()">
  ${form.render(buttons=capture(self.render_form_buttons))|n}
</%def>

<%def name="render_buefy_form()">
  <div class="form">
    ${form.render_vuejs_component()}
  </div>
</%def>

<%def name="page_content()">
  <div class="form-wrapper">
    <br />
    ${self.render_buefy_form()}
  </div>
</%def>

<%def name="render_this_page()">
  <div style="display: flex; justify-content: space-between;">

    <div class="this-page-content">
      ${self.page_content()}
    </div>

    <div style="display: flex; align-items: flex-start;">

      ${before_object_helpers()}

      <div class="object-helpers">
        ${self.object_helpers()}
      </div>

      <ul id="context-menu">
        ${self.context_menu_items()}
      </ul>
    </div>

  </div>
</%def>

<%def name="before_object_helpers()"></%def>

<%def name="render_this_page_template()">
  % if form is not Undefined:
      ${self.render_form()}
  % endif
  ${parent.render_this_page_template()}
</%def>

<%def name="finalize_this_page_vars()">
  ${parent.finalize_this_page_vars()}
  % if form is not Undefined:
      <script type="text/javascript">

        ${form.component_studly}.data = function() { return ${form.component_studly}Data }

        Vue.component('${form.component}', ${form.component_studly})

      </script>
  % endif
</%def>


${parent.body()}
