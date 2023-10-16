## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">

  <h3 class="block is-size-3">Basics</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field grouped>

      <b-field label="App Title">
        <b-input name="rattail.app_title"
                 v-model="simpleSettings['rattail.app_title']"
                 @input="settingsNeedSaved = true">
        </b-input>
      </b-field>

      <b-field label="Node Type">
        ## TODO: should be a dropdown, app handler defines choices
        <b-input name="rattail.node_type"
                 v-model="simpleSettings['rattail.node_type']"
                 @input="settingsNeedSaved = true">
        </b-input>
      </b-field>

      <b-field label="Node Title">
        <b-input name="rattail.node_title"
                 v-model="simpleSettings['rattail.node_title']"
                 @input="settingsNeedSaved = true">
        </b-input>
      </b-field>

    </b-field>

    <b-field>
      <b-checkbox name="rattail.production"
                  v-model="simpleSettings['rattail.production']"
                  native-value="true"
                  @input="settingsNeedSaved = true">
        Production Mode
      </b-checkbox>
    </b-field>

    <div class="level-left">
      <div class="level-item">
        <b-field>
          <b-checkbox name="rattail.running_from_source"
                      v-model="simpleSettings['rattail.running_from_source']"
                      native-value="true"
                      @input="settingsNeedSaved = true">
            Running from Source
          </b-checkbox>
        </b-field>
      </div>
      <div class="level-item">
        <b-field label="Top-Level Package" horizontal
                 v-if="simpleSettings['rattail.running_from_source']">
          <b-input name="rattail.running_from_source.rootpkg"
                   v-model="simpleSettings['rattail.running_from_source.rootpkg']"
                   @input="settingsNeedSaved = true">
          </b-input>
        </b-field>
      </div>
    </div>

  </div>

  <h3 class="block is-size-3">Display</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field grouped>

      <b-field label="Background Color">
        <b-input name="tailbone.background_color"
                 v-model="simpleSettings['tailbone.background_color']"
                 @input="settingsNeedSaved = true">
        </b-input>
      </b-field>

    </b-field>

  </div>

  <h3 class="block is-size-3">Grids</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field grouped>

      <b-field label="Default Page Size">
        <b-input name="tailbone.grid.default_pagesize"
                 v-model="simpleSettings['tailbone.grid.default_pagesize']"
                 @input="settingsNeedSaved = true">
        </b-input>
      </b-field>

    </b-field>

  </div>

  <h3 class="block is-size-3">Web Libraries</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-table :data="weblibs">

      <b-table-column field="title"
                      label="Name"
                      v-slot="props">
        {{ props.row.title }}
      </b-table-column>

      <b-table-column field="configured_version"
                      label="Version"
                      v-slot="props">
        {{ props.row.configured_version || props.row.default_version }}
      </b-table-column>

      <b-table-column field="configured_url"
                      label="URL Override"
                      v-slot="props">
        {{ props.row.configured_url }}
      </b-table-column>

      <b-table-column field="live_url"
                      label="Effective (Live) URL"
                      v-slot="props">
        <span v-if="props.row.modified"
              class="has-text-warning">
          save settings and refresh page to see new URL
        </span>
        <span v-if="!props.row.modified">
          {{ props.row.live_url }}
        </span>
      </b-table-column>

      <b-table-column field="actions"
                      label="Actions"
                      v-slot="props">
        <a href="#"
           @click.prevent="editWebLibraryInit(props.row)">
          <i class="fas fa-edit"></i>
          Edit
        </a>
      </b-table-column>

    </b-table>

    % for weblib in weblibs:
        ${h.hidden('tailbone.libver.{}'.format(weblib['key']), **{':value': "simpleSettings['tailbone.libver.{}']".format(weblib['key'])})}
        ${h.hidden('tailbone.liburl.{}'.format(weblib['key']), **{':value': "simpleSettings['tailbone.liburl.{}']".format(weblib['key'])})}
    % endfor

    <b-modal has-modal-card
             :active.sync="editWebLibraryShowDialog">
      <div class="modal-card">

        <header class="modal-card-head">
          <p class="modal-card-title">Web Library: {{ editWebLibraryRecord.title }}</p>
        </header>

        <section class="modal-card-body">

          <b-field grouped>
            
            <b-field label="Default Version">
              <b-input v-model="editWebLibraryRecord.default_version"
                       disabled>
              </b-input>
            </b-field>

            <b-field label="Override Version">
              <b-input v-model="editWebLibraryVersion">
              </b-input>
            </b-field>

          </b-field>

          <b-field label="Override URL">
            <b-input v-model="editWebLibraryURL">
            </b-input>
          </b-field>

          <b-field label="Effective URL (as of last page load)">
            <b-input v-model="editWebLibraryRecord.live_url"
                     disabled>
            </b-input>
          </b-field>

        </section>

        <footer class="modal-card-foot">
          <b-button type="is-primary"
                    @click="editWebLibrarySave()"
                    icon-pack="fas"
                    icon-left="save">
            Save
          </b-button>
          <b-button @click="editWebLibraryShowDialog = false">
            Cancel
          </b-button>
        </footer>
      </div>
    </b-modal>

  </div>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.weblibs = ${json.dumps(weblibs)|n}

    ThisPageData.editWebLibraryShowDialog = false
    ThisPageData.editWebLibraryRecord = {}
    ThisPageData.editWebLibraryVersion = null
    ThisPageData.editWebLibraryURL = null

    ThisPage.methods.editWebLibraryInit = function(row) {
        this.editWebLibraryRecord = row
        this.editWebLibraryVersion = row.configured_version
        this.editWebLibraryURL = row.configured_url
        this.editWebLibraryShowDialog = true
    }

    ThisPage.methods.editWebLibrarySave = function() {
        this.editWebLibraryRecord.configured_version = this.editWebLibraryVersion
        this.editWebLibraryRecord.configured_url = this.editWebLibraryURL
        this.editWebLibraryRecord.modified = true

        this.simpleSettings[`tailbone.libver.${'$'}{this.editWebLibraryRecord.key}`] = this.editWebLibraryVersion
        this.simpleSettings[`tailbone.liburl.${'$'}{this.editWebLibraryRecord.key}`] = this.editWebLibraryURL

        this.settingsNeedSaved = true
        this.editWebLibraryShowDialog = false
    }

  </script>
</%def>


${parent.body()}
