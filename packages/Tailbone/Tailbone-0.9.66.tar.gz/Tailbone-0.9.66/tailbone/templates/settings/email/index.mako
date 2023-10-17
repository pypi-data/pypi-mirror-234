## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="render_grid_component()">
  % if master.has_perm('configure'):
      <b-field horizontal label="Showing:">
        <b-select v-model="showEmails" @input="updateVisibleEmails()">
          <option value="available">Available Emails</option>
          <option value="all">All Emails</option>
          <option value="hidden">Hidden Emails</option>
        </b-select>
      </b-field>
  % endif

  ${parent.render_grid_component()}
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  % if master.has_perm('configure'):
      <script type="text/javascript">

        ThisPageData.showEmails = 'available'

        ThisPage.methods.updateVisibleEmails = function() {
            this.$refs.grid.showEmails = this.showEmails
        }

        ${grid.component_studly}Data.showEmails = 'available'

        ${grid.component_studly}.computed.visibleData = function() {

            if (this.showEmails == 'available') {
                return this.data.filter(email => email.hidden == 'No')

            } else if (this.showEmails == 'hidden') {
                return this.data.filter(email => email.hidden == 'Yes')
            }

            // showing all
            return this.data
        }

        ${grid.component_studly}.methods.renderLabelToggleHidden = function(row) {
            return row.hidden == 'Yes' ? "Un-hide" : "Hide"
        }

        ${grid.component_studly}.methods.toggleHidden = function(row) {
            let url = '${url('{}.toggle_hidden'.format(route_prefix))}'
            let params = {
                key: row.key,
                hidden: row.hidden == 'No'? true : false,
            }
            this.submitForm(url, params, response => {
                row.hidden = params.hidden ? 'Yes' : 'No'
            })
        }

      </script>
  % endif
</%def>

${parent.body()}
