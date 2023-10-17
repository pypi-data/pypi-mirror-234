## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('datasync.status'):
      <li>${h.link_to("View DataSync Status", url('datasync.status'))}</li>
  % endif
</%def>

<%def name="grid_tools()">
  ${parent.grid_tools()}

  % if request.has_perm('datasync.restart'):
      ${h.form(url('datasync.restart'), name='restart-datasync', class_='control', **{'@submit': 'submitRestartDatasyncForm'})}
      ${h.csrf_token(request)}
      <b-button native-type="submit"
                :disabled="restartDatasyncFormSubmitting">
        {{ restartDatasyncFormButtonText }}
      </b-button>
      ${h.end_form()}
  % endif

  % if allow_filemon_restart and request.has_perm('filemon.restart'):
      ${h.form(url('filemon.restart'), name='restart-filemon', class_='control', **{'@submit': 'submitRestartFilemonForm'})}
      ${h.csrf_token(request)}
      <b-button native-type="submit"
                :disabled="restartFilemonFormSubmitting">
        {{ restartFilemonFormButtonText }}
      </b-button>
      ${h.end_form()}
  % endif

</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if request.has_perm('datasync.restart'):
        TailboneGridData.restartDatasyncFormSubmitting = false
        TailboneGridData.restartDatasyncFormButtonText = "Restart Datasync"
        TailboneGrid.methods.submitRestartDatasyncForm = function() {
            this.restartDatasyncFormSubmitting = true
            this.restartDatasyncFormButtonText = "Restarting Datasync..."
        }
    % endif

    % if allow_filemon_restart and request.has_perm('filemon.restart'):
        TailboneGridData.restartFilemonFormSubmitting = false
        TailboneGridData.restartFilemonFormButtonText = "Restart Filemon"
        TailboneGrid.methods.submitRestartFilemonForm = function() {
            this.restartFilemonFormSubmitting = true
            this.restartFilemonFormButtonText = "Restarting Filemon..."
        }
    % endif

  </script>
</%def>


${parent.body()}
