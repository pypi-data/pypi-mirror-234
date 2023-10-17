## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':
      <script type="text/javascript">

        ThisPage.methods.deleteObject = function() {
            if (confirm("Are you sure you wish to delete this ${model_title}?")) {
                this.$refs.deleteObjectForm.submit()
            }
        }

      </script>
  % endif
</%def>


${parent.body()}
