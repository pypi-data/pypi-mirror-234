## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />
<%namespace file="/util.mako" import="view_profiles_helper" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  % if show_profiles_helper and show_profiles_people:
      ${view_profiles_helper(show_profiles_people)}
  % endif
</%def>

<%def name="render_buefy_form()">
  <div class="form">
    <tailbone-form @detach-person="detachPerson">
    </tailbone-form>
  </div>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if expose_shoppers:
    ${form.component_studly}Data.shoppers = ${json.dumps(shoppers_data)|n}
    % endif
    % if expose_people:
    ${form.component_studly}Data.peopleData = ${json.dumps(people_data)|n}
    % endif

    ThisPage.methods.detachPerson = function(url) {
        ## TODO: this should require POST, but we will add that once
        ## we can assume a Buefy theme is present, to avoid having to
        ## implement the logic in old jquery...
        if (confirm("Are you sure you want to detach this person from this customer account?")) {
            location.href = url
        }
    }

  </script>
</%def>

${parent.body()}
