## -*- coding: utf-8; -*-
<%inherit file="/master/form.mako" />

<%def name="title()">${index_title} &raquo; ${instance_title}</%def>

<%def name="content_title()">
  ${instance_title}
</%def>

<%def name="render_instance_header_title_extras()">
  <span style="width: 2rem;"></span>
  % if master.touchable and master.has_perm('touch'):
      <b-button title="&quot;Touch&quot; this record to trigger sync"
                icon-pack="fas"
                icon-left="hand-pointer"
                @click="touchRecord()"
                :disabled="touchSubmitting">
      </b-button>
  % endif
</%def>

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ${self.render_xref_helper()}
</%def>

<%def name="render_xref_helper()">
  % if xref_buttons or xref_links:
      <nav class="panel">
        <p class="panel-heading">Cross-Reference</p>
        <div class="panel-block buttons">
          <div style="display: flex; flex-direction: column;">
            % for button in xref_buttons:
                ${button}
            % endfor
            % for link in xref_links:
                ${link}
            % endfor
          </div>
        </div>
      </nav>
  % endif
</%def>

<%def name="context_menu_items()">
  ## TODO: either make this configurable, or just lose it.
  ## nobody seems to ever find it useful in practice.
  ## <li>${h.link_to("Permalink for this {}".format(model_title), action_url('view', instance))}</li>
  % if master.has_versions and request.rattail_config.versioning_enabled() and request.has_perm('{}.versions'.format(permission_prefix)):
      <li>${h.link_to("Version History", action_url('versions', instance))}</li>
  % endif
</%def>

<%def name="render_row_grid_tools()">
  ${rows_grid_tools}
  % if master.rows_downloadable_xlsx and master.has_perm('row_results_xlsx'):
      <b-button tag="a" href="${master.get_action_url('row_results_xlsx', instance)}"
                icon-pack="fas"
                icon-left="download">
        Download Results XLSX
      </b-button>
  % endif
  % if master.rows_downloadable_csv and master.has_perm('row_results_csv'):
      <b-button tag="a" href="${master.get_action_url('row_results_csv', instance)}"
                icon-pack="fas"
                icon-left="download">
        Download Results CSV
      </b-button>
  % endif
</%def>

<%def name="render_this_page()">
  ${parent.render_this_page()}
  % if master.has_rows:
      <br />
      % if rows_title:
          <h4 class="block is-size-4">${rows_title}</h4>
      % endif
      ${self.render_row_grid_component()}
  % endif
</%def>

<%def name="render_row_grid_component()">
  <tailbone-grid ref="rowGrid" id="rowGrid"></tailbone-grid>
</%def>

<%def name="render_this_page_template()">
  % if master.has_rows:
      ## TODO: stop using |n filter
      ${rows_grid.render_buefy(allow_save_defaults=False, tools=capture(self.render_row_grid_tools))|n}
  % endif
  ${parent.render_this_page_template()}
</%def>

<%def name="modify_whole_page_vars()">
  ${parent.modify_whole_page_vars()}
  % if master.touchable and master.has_perm('touch'):
      <script type="text/javascript">

        WholePageData.touchSubmitting = false

        WholePage.methods.touchRecord = function() {
            this.touchSubmitting = true
            location.href = '${master.get_action_url('touch', instance)}'
        }

      </script>
  % endif
</%def>

<%def name="finalize_this_page_vars()">
  ${parent.finalize_this_page_vars()}
  % if master.has_rows:
  <script type="text/javascript">

    TailboneGrid.data = function() { return TailboneGridData }

    Vue.component('tailbone-grid', TailboneGrid)

  </script>
  % endif
</%def>


${parent.body()}
