## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="title()">Delete ${model_title}: ${instance_title}</%def>

<%def name="render_buefy_form()">
  <br />
  <b-notification type="is-danger" :closable="false">
    You are about to delete the following ${model_title} and all associated data:
  </b-notification>
  ${parent.render_buefy_form()}
</%def>

<%def name="render_form_buttons()">
  <br />
  <b-notification type="is-danger" :closable="false">
    Are you sure about this?
  </b-notification>
  <br />

  ${h.form(request.current_route_url(), **{'@submit': 'submitForm'})}
  ${h.csrf_token(request)}
    <div class="buttons">
      <once-button tag="a" href="${form.cancel_url}"
                   text="Whoops, nevermind...">
      </once-button>
      <b-button type="is-primary is-danger"
                native-type="submit"
                :disabled="formSubmitting">
        {{ formButtonText }}
      </b-button>
    </div>
  ${h.end_form()}
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    TailboneFormData.formSubmitting = false
    TailboneFormData.formButtonText = "Yes, please DELETE this data forever!"

    TailboneForm.methods.submitForm = function() {
        this.formSubmitting = true
        this.formButtonText = "Working, please wait..."
    }

  </script>
</%def>


${parent.body()}
