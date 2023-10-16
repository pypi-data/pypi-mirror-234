## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">Find ${model_title_plural} by Permission</%def>

<%def name="page_content()">
  <br />
  <find-principals :permission-groups="permissionGroups"
                   :sorted-groups="sortedGroups">
  </find-principals>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  <script type="text/x-template" id="find-principals-template">
    <div>

      ${h.form(request.current_route_url(), method='GET', **{'@submit': 'formSubmitting = true'})}

      <b-field label="Permission Group" horizontal>
        <b-select name="permission_group"
                  v-model="selectedGroup"
                  @input="selectGroup">
          <option v-for="groupkey in sortedGroups"
                  :key="groupkey"
                  :value="groupkey">
            {{ permissionGroups[groupkey].label }}
          </option>
        </b-select>
      </b-field>

      <b-field label="Permission" horizontal>
        <b-select name="permission"
                  v-model="selectedPermission">
          <option v-for="perm in groupPermissions"
                  :key="perm.permkey"
                  :value="perm.permkey">
            {{ perm.label }}
          </option>
        </b-select>
      </b-field>

      <div class="buttons">
        <once-button tag="a"
                     href="${request.current_route_url(_query=None)}"
                     text="Reset Form">
        </once-button>
        <b-button type="is-primary"
                  native-type="submit"
                  icon-pack="fas"
                  icon-left="search"
                  :disabled="formSubmitting">
          {{ formSubmitting ? "Working, please wait..." : "Find ${model_title_plural}" }}
        </b-button>
      </div>

      ${h.end_form()}

      % if principals is not None:
      <div class="grid half">
        <br />
        <h2>Found ${len(principals)} ${model_title_plural} with permission: ${selected_permission}</h2>
        ${self.principal_table()}
      </div>
      % endif

    </div>
  </script>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.permissionGroups = ${json.dumps(buefy_perms)|n}
    ThisPageData.sortedGroups = ${json.dumps(buefy_sorted_groups)|n}

  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    Vue.component('find-principals', {
        template: '#find-principals-template',
        props: {
            permissionGroups: Object,
            sortedGroups: Array
        },
        data() {
            return {
                groupPermissions: ${json.dumps(buefy_perms.get(selected_group, {}).get('permissions', []))|n},
                selectedGroup: ${json.dumps(selected_group)|n},
                % if selected_permission:
                selectedPermission: ${json.dumps(selected_permission)|n},
                % elif selected_group in buefy_perms:
                selectedPermission: ${json.dumps(buefy_perms[selected_group]['permissions'][0]['permkey'])|n},
                % else:
                selectedPermission: null,
                % endif
                formSubmitting: false,
            }
        },
        methods: {

            selectGroup(groupkey) {

                // re-populate Permission dropdown, auto-select first option
                this.groupPermissions = this.permissionGroups[groupkey].permissions
                this.selectedPermission = this.groupPermissions[0].permkey
            },
        }
    })

  </script>
</%def>


${parent.body()}
