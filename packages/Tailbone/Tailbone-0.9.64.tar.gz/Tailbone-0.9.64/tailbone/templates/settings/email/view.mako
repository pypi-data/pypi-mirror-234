## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="render_buefy_form()">
  ${parent.render_buefy_form()}
  <email-preview-tools></email-preview-tools>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  <script type="text/x-template" id="email-preview-tools-template">

  ${h.form(url('email.preview'), **{'@submit': 'submitPreviewForm'})}
    ${h.csrf_token(request)}
    ${h.hidden('email_key', value=instance['key'])}

    <br />

    <div class="field is-grouped">

      <div class="control">
        % if email.get_template('html'):
            <a class="button is-primary"
               href="${url('email.preview')}?key=${instance['key']}&type=html"
               target="_blank">
              Preview HTML
            </a>
        % else:
            <button class="button is-primary"
                    type="button"
                    title="There is no HTML template on file for this email."
                    disabled>
              Preview HTML
            </button>
        % endif
      </div>

      <div class="control">
      % if email.get_template('txt'):
          <a class="button is-primary"
             href="${url('email.preview')}?key=${instance['key']}&type=txt"
             target="_blank">
            Preview TXT
          </a>
      % else:
          <button class="button is-primary"
                  type="button"
                  title="There is no TXT template on file for this email."
                  disabled>
            Preview TXT
          </button>
      % endif
      </div>

      <div class="control">
        or
      </div>

      <div class="control">
        <b-input name="recipient" v-model="userEmailAddress"></b-input>
      </div>

      <div class="control">
        <b-button type="is-primary"
                  native-type="submit"
                  :disabled="previewFormSubmitting">
          {{ previewFormButtonText }}
        </b-button>
      </div>

    </div><!-- field -->

  ${h.end_form()}
  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    const EmailPreviewTools = {
        template: '#email-preview-tools-template',
        data() {
            return {
                previewFormButtonText: "Send Preview Email",
                previewFormSubmitting: false,
                userEmailAddress: ${json.dumps(user_email_address)|n},
            }
        },
        methods: {
            submitPreviewForm(event) {
                if (!this.userEmailAddress) {
                    alert("Please provide an email address.")
                    event.preventDefault()
                    return
                }
                this.previewFormSubmitting = true
                this.previewFormButtonText = "Working, please wait..."
            }
        }
    }

    Vue.component('email-preview-tools', EmailPreviewTools)

  </script>
</%def>


${parent.body()}
