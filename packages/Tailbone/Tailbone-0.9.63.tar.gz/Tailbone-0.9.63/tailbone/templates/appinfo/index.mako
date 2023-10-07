## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="render_grid_component()">

  <div class="buttons">

    <once-button type="is-primary"
                 tag="a" href="${url('tables')}"
                 icon-pack="fas"
                 icon-left="eye"
                 text="Tables">
    </once-button>

    <once-button type="is-primary"
                 tag="a" href="${url('model_views')}"
                 icon-pack="fas"
                 icon-left="eye"
                 text="Model Views">
    </once-button>

    <once-button type="is-primary"
                 tag="a" href="${url('configure_menus')}"
                 icon-pack="fas"
                 icon-left="cog"
                 text="Configure Menus">
    </once-button>

  </div>

  <b-collapse class="panel" open>

    <template #trigger="props">
      <div class="panel-heading"
           role="button">

        ## TODO: for some reason buefy will "reuse" the icon
        ## element in such a way that its display does not
        ## refresh.  so to work around that, we use different
        ## structure for the two icons, so buefy is forced to
        ## re-draw

        <b-icon v-if="props.open"
                pack="fas"
                icon="angle-down">
        </b-icon>

        <span v-if="!props.open">
          <b-icon pack="fas"
                  icon="angle-right">
          </b-icon>
        </span>

        <strong>Configuration Files</strong>
      </div>
    </template>

    <div class="panel-block">
      <div style="width: 100%;">
        <b-table :data="configFiles">
          
          <b-table-column field="priority"
                          label="Priority"
                          v-slot="props">
            {{ props.row.priority }}
          </b-table-column>

          <b-table-column field="path"
                          label="File Path"
                          v-slot="props">
            {{ props.row.path }}
          </b-table-column>

        </b-table>
      </div>
    </div>
  </b-collapse>

  <b-collapse class="panel"
              :open="false">

    <template #trigger="props">
      <div class="panel-heading"
           role="button">

        ## TODO: for some reason buefy will "reuse" the icon
        ## element in such a way that its display does not
        ## refresh.  so to work around that, we use different
        ## structure for the two icons, so buefy is forced to
        ## re-draw

        <b-icon v-if="props.open"
                pack="fas"
                icon="angle-down">
        </b-icon>

        <span v-if="!props.open">
          <b-icon pack="fas"
                  icon="angle-right">
          </b-icon>
        </span>

        <strong>Installed Packages</strong>
      </div>
    </template>

    <div class="panel-block">
      <div style="width: 100%;">
        ${parent.render_grid_component()}
      </div>
    </div>
  </b-collapse>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.configFiles = ${json.dumps([dict(path=p, priority=i) for i, p in enumerate(reversed(request.rattail_config.files_read), 1)])|n}

  </script>
</%def>


${parent.body()}
