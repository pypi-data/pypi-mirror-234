## -*- coding: utf-8; -*-

<script type="text/x-template" id="grid-filter-numeric-value-template">
  <div class="level">
    <div class="level-left">
      <div class="level-item">
        <b-input v-model="startValue"
                 ref="startValue"
                 @input="startValueChanged">
        </b-input>
      </div>
      <div v-show="wantsRange"
           class="level-item">
        and
      </div>
      <div v-show="wantsRange"
           class="level-item">
        <b-input v-model="endValue"
                 ref="endValue"
                 @input="endValueChanged">
        </b-input>
      </div>
    </div>
  </div>
</script>

<script type="text/x-template" id="grid-filter-date-value-template">
  <div class="level">
    <div class="level-left">
      <div class="level-item">
        <tailbone-datepicker v-model="startDate"
                             ref="startDate"
                             @input="startDateChanged">
        </tailbone-datepicker>
      </div>
      <div v-show="dateRange"
           class="level-item">
        and
      </div>
      <div v-show="dateRange"
           class="level-item">
        <tailbone-datepicker v-model="endDate"
                             ref="endDate"
                             @input="endDateChanged">
        </tailbone-datepicker>
      </div>
    </div>
  </div>
</script>

<script type="text/x-template" id="grid-filter-template">

  <div class="level filter" v-show="filter.visible">
    <div class="level-left"
         style="align-items: start;">

      <div class="level-item filter-fieldname">

        <b-field>
          <b-checkbox-button v-model="filter.active" native-value="IGNORED">
            <b-icon pack="fas" icon="check" v-show="filter.active"></b-icon>
            <span>{{ filter.label }}</span>
          </b-checkbox-button>
        </b-field>

      </div>

      <b-field grouped v-show="filter.active"
               class="level-item"
               style="align-items: start;">

        <b-select v-model="filter.verb"
                  @input="focusValue()"
                  class="filter-verb">
          <option v-for="verb in filter.verbs"
                  :key="verb"
                  :value="verb">
            {{ filter.verb_labels[verb] }}
          </option>
        </b-select>

        ## only one of the following "value input" elements will be rendered

        <grid-filter-date-value v-if="filter.data_type == 'date'"
                                v-model="filter.value"
                                v-show="valuedVerb()"
                                :date-range="filter.verb == 'between'"
                                ref="valueInput">
        </grid-filter-date-value>

        <b-select v-if="filter.data_type == 'choice'"
                  v-model="filter.value"
                  v-show="valuedVerb()"
                  ref="valueInput">
          <option v-for="choice in filter.choices"
                  :key="choice"
                  :value="choice">
            {{ filter.choice_labels[choice] || choice }}
          </option>
        </b-select>

        <grid-filter-numeric-value v-if="filter.data_type == 'number'"
                                  v-model="filter.value"
                                  v-show="valuedVerb()"
                                  :wants-range="filter.verb == 'between'"
                                  ref="valueInput">
        </grid-filter-numeric-value>

        <b-input v-if="filter.data_type == 'string' && !multiValuedVerb()"
                 v-model="filter.value"
                 v-show="valuedVerb()"
                 ref="valueInput">
        </b-input>

        <b-input v-if="filter.data_type == 'string' && multiValuedVerb()"
                 type="textarea"
                 v-model="filter.value"
                 v-show="valuedVerb()"
                 ref="valueInput">
        </b-input>

      </b-field>

    </div><!-- level-left -->
  </div><!-- level -->

</script>

<script type="text/x-template" id="${grid.component}-template">
  <div>

    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5em;">

      <div style="display: flex; flex-direction: column; justify-content: space-between;">
        <div></div>
        <div class="filters">
          % if grid.filterable:
              ## TODO: stop using |n filter
              ${grid.render_filters(template='/grids/filters_buefy.mako', allow_save_defaults=allow_save_defaults)|n}
          % endif
        </div>
      </div>

      <div style="display: flex; flex-direction: column; justify-content: space-between;">

        <div class="context-menu">
          % if context_menu:
              <ul id="context-menu">
                ## TODO: stop using |n filter
                ${context_menu|n}
              </ul>
          % endif
        </div>

        <div class="grid-tools-wrapper">
          % if tools:
              <div class="grid-tools field buttons is-grouped is-pulled-right">
                ## TODO: stop using |n filter
                ${tools|n}
              </div>
          % endif
        </div>

      </div>

    </div>

    <b-table
       :data="visibleData"
       ## :columns="columns"
       :loading="loading"
       :row-class="getRowClass"

       ## TODO: this should be more configurable, maybe auto-detect based
       ## on buefy version??  probably cannot do that, but this feature
       ## is only supported with buefy 0.8.13 and newer
       % if request.rattail_config.getbool('tailbone', 'sticky_headers'):
       sticky-header
       height="600px"
       % endif

       :checkable="checkable"

       % if grid.checkboxes:
       :checked-rows.sync="checkedRows"
       % if grid.clicking_row_checks_box:
       @click="rowClick"
       % endif
       % endif

       % if grid.check_handler:
       @check="${grid.check_handler}"
       % endif
       % if grid.check_all_handler:
       @check-all="${grid.check_all_handler}"
       % endif

       % if isinstance(grid.checkable, str):
       :is-row-checkable="${grid.row_checkable}"
       % elif grid.checkable:
       :is-row-checkable="row => row._checkable"
       % endif

       % if grid.sortable:
           backend-sorting
           @sort="onSort"
           @sorting-priority-removed="sortingPriorityRemoved"

           ## TODO: there is a bug (?) which prevents the arrow from
           ## displaying for simple default single-column sort.  so to
           ## work around that, we *disable* multi-sort until the
           ## component is mounted.  seems to work for now..see also
           ## https://github.com/buefy/buefy/issues/2584
           :sort-multiple="allowMultiSort"

           ## nb. specify default sort only if single-column
           :default-sort="backendSorters.length == 1 ? [backendSorters[0].field, backendSorters[0].order] : null"

           ## nb. otherwise there may be default multi-column sort
           :sort-multiple-data="sortingPriority"

           ## user must ctrl-click column header to do multi-sort
           sort-multiple-key="ctrlKey"
       % endif

       % if grid.click_handlers:
       @cellclick="cellClick"
       % endif

       :paginated="paginated"
       :per-page="perPage"
       :current-page="currentPage"
       backend-pagination
       :total="total"
       @page-change="onPageChange"

       ## TODO: should let grid (or master view) decide how to set these?
       icon-pack="fas"
       ## note that :striped="true" was interfering with row status (e.g. warning) styles
       :striped="false"
       :hoverable="true"
       :narrowed="true">

      % for column in grid_columns:
          <b-table-column field="${column['field']}"
                          label="${column['label']}"
                          v-slot="props"
                          :sortable="${json.dumps(column['sortable'])}"
                          % if grid.is_searchable(column['field']):
                          searchable
                          % endif
                          cell-class="c_${column['field']}"
                          :visible="${json.dumps(column['visible'])}">
            % if column['field'] in grid.raw_renderers:
                ${grid.raw_renderers[column['field']]()}
            % elif grid.is_linked(column['field']):
                <a :href="props.row._action_url_view"
                   % if view_click_handler:
                   @click.prevent="${view_click_handler}"
                   % endif
                   v-html="props.row.${column['field']}">
                </a>
            % else:
                <span v-html="props.row.${column['field']}"></span>
            % endif
          </b-table-column>
      % endfor

      % if grid.main_actions or grid.more_actions:
          <b-table-column field="actions"
                          label="Actions"
                          v-slot="props">
            ## TODO: we do not currently differentiate for "main vs. more"
            ## here, but ideally we would tuck "more" away in a drawer etc.
            % for action in grid.main_actions + grid.more_actions:
                <a v-if="props.row._action_url_${action.key}"
                   :href="props.row._action_url_${action.key}"
                   class="grid-action${' has-text-danger' if action.key == 'delete' else ''} ${action.link_class or ''}"
                   % if action.click_handler:
                   @click.prevent="${action.click_handler}"
                   % endif
                   % if action.target:
                   target="${action.target}"
                   % endif
                   >
                  ${action.render_icon()|n}
                  ${action.render_label()|n}
                </a>
                &nbsp;
            % endfor
          </b-table-column>
      % endif

      <template #empty>
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p>
              <b-icon
                 pack="fas"
                 icon="fas fa-sad-tear"
                 size="is-large">
              </b-icon>
            </p>
            <p>Nothing here.</p>
          </div>
        </section>
      </template>

      <template #footer>
        <div style="display: flex; justify-content: space-between;">

          % if grid.expose_direct_link:
              <b-button type="is-primary"
                        size="is-small"
                        @click="copyDirectLink()"
                        title="Copy link to clipboard">
                <span><i class="fa fa-share-alt"></i></span>
              </b-button>
          % else:
              <div></div>
          % endif

          % if grid.pageable:
              <b-field grouped
                       v-if="firstItem">
                <span class="control">
                  showing {{ firstItem.toLocaleString('en') }} - {{ lastItem.toLocaleString('en') }} of {{ total.toLocaleString('en') }} results;
                </span>
                <b-select v-model="perPage"
                          size="is-small"
                          @input="loadAsyncData()">
                  % for value in grid.get_pagesize_options():
                      <option value="${value}">${value}</option>
                  % endfor
                </b-select>
                <span class="control">
                  per page
                </span>
              </b-field>
          % endif

        </div>
      </template>

    </b-table>

    ## dummy input field needed for sharing links on *insecure* sites
    % if request.scheme == 'http':
        <b-input v-model="shareLink" ref="shareLink" v-show="shareLink"></b-input>
    % endif

  </div>
</script>

<script type="text/javascript">

  let ${grid.component_studly}CurrentData = ${json.dumps(grid_data['data'])|n}

  let ${grid.component_studly}Data = {
      loading: false,
      ajaxDataUrl: ${json.dumps(grid.ajax_data_url)|n},

      data: ${grid.component_studly}CurrentData,
      rowStatusMap: ${json.dumps(grid_data['row_status_map'])|n},

      checkable: ${json.dumps(grid.checkboxes)|n},
      % if grid.checkboxes:
      checkedRows: ${grid_data['checked_rows_code']|n},
      % endif

      paginated: ${json.dumps(grid.pageable)|n},
      total: ${len(grid_data['data']) if static_data else grid_data['total_items']},
      perPage: ${json.dumps(grid.pagesize if grid.pageable else None)|n},
      currentPage: ${json.dumps(grid.page if grid.pageable else None)|n},
      firstItem: ${json.dumps(grid_data['first_item'] if grid.pageable else None)|n},
      lastItem: ${json.dumps(grid_data['last_item'] if grid.pageable else None)|n},

      % if grid.sortable:

          ## TODO: there is a bug (?) which prevents the arrow from
          ## displaying for simple default single-column sort.  so to
          ## work around that, we *disable* multi-sort until the
          ## component is mounted.  seems to work for now..see also
          ## https://github.com/buefy/buefy/issues/2584
          allowMultiSort: false,

          ## nb. this contains all truly active sorters
          backendSorters: ${json.dumps(grid.active_sorters)|n},

          ## nb. whereas this will only contain multi-column sorters,
          ## but will be *empty* for single-column sorting
          % if len(grid.active_sorters) > 1:
              sortingPriority: ${json.dumps(grid.active_sorters)|n},
          % else:
              sortingPriority: [],
          % endif

      % endif

      ## filterable: ${json.dumps(grid.filterable)|n},
      filters: ${json.dumps(filters_data if grid.filterable else None)|n},
      filtersSequence: ${json.dumps(filters_sequence if grid.filterable else None)|n},
      addFilterTerm: '',
      addFilterShow: false,

      ## dummy input value needed for sharing links on *insecure* sites
      % if request.scheme == 'http':
      shareLink: null,
      % endif
  }

  let ${grid.component_studly} = {
      template: '#${grid.component}-template',

      mixins: [FormPosterMixin],

      props: {
          csrftoken: String,
      },

      computed: {

          addFilterChoices() {

              // collect all filters, which are *not* already shown
              let choices = []
              for (let field of this.filtersSequence) {
                  let filtr = this.filters[field]
                  if (!filtr.visible) {
                      choices.push(filtr)
                  }
              }

              // parse list of search terms
              let terms = []
              for (let term of this.addFilterTerm.toLowerCase().split(' ')) {
                  term = term.trim()
                  if (term) {
                      terms.push(term)
                  }
              }

              // only filters matching all search terms are presented
              // as choices to the user
              return choices.filter(option => {
                  let label = option.label.toLowerCase()
                  for (let term of terms) {
                      if (label.indexOf(term) < 0) {
                          return false
                      }
                  }
                  return true
              })
          },

          // note, can use this with v-model for hidden 'uuids' fields
          selected_uuids: function() {
              return this.checkedRowUUIDs().join(',')
          },

          // nb. this can be overridden if needed, e.g. to dynamically
          // show/hide certain records in a static data set
          visibleData() {
              return this.data
          },

          directLink() {
              let params = new URLSearchParams(this.getAllParams())
              return `${request.current_route_url(_query=None)}?${'$'}{params}`
          },
      },

      mounted() {
          ## TODO: there is a bug (?) which prevents the arrow from
          ## displaying for simple default single-column sort.  so to
          ## work around that, we *disable* multi-sort until the
          ## component is mounted.  seems to work for now..see also
          ## https://github.com/buefy/buefy/issues/2584
          this.allowMultiSort = true
      },

      methods: {

          % if grid.click_handlers:
              cellClick(row, column, rowIndex, columnIndex) {
                  % for key in grid.click_handlers:
                      if (column._props.field == '${key}') {
                          ${grid.click_handlers[key]}(row)
                      }
                  % endfor
              },
          % endif

          copyDirectLink() {

              if (navigator.clipboard) {
                  // this is the way forward, but requires HTTPS
                  navigator.clipboard.writeText(this.directLink)

              } else {
                  // use deprecated 'copy' command, but this just
                  // tells the browser to copy currently-selected
                  // text..which means we first must "add" some text
                  // to screen, and auto-select that, before copying
                  // to clipboard
                  this.shareLink = this.directLink
                  this.$nextTick(() => {
                      let input = this.$refs.shareLink.$el.firstChild
                      input.select()
                      document.execCommand('copy')
                      // re-hide the dummy input
                      this.shareLink = null
                  })
              }

              this.$buefy.toast.open({
                  message: "Link was copied to clipboard",
                  type: 'is-info',
                  duration: 2000, // 2 seconds
              })
          },

          addRowClass(index, className) {

              // TODO: this may add duplicated name to class string
              // (not a serious problem i think, but could be improved)
              this.rowStatusMap[index] = (this.rowStatusMap[index] || '')
                  + ' ' + className

              // nb. for some reason b-table does not always "notice"
              // when we update status; so we force it to refresh
              this.$forceUpdate()
          },

          getRowClass(row, index) {
              return this.rowStatusMap[index]
          },

          getBasicParams() {
              let params = {}
              % if grid.sortable:
                  for (let i = 1; i <= this.backendSorters.length; i++) {
                      params['sort'+i+'key'] = this.backendSorters[i-1].field
                      params['sort'+i+'dir'] = this.backendSorters[i-1].order
                  }
              % endif
              % if grid.pageable:
                  params.pagesize = this.perPage
                  params.page = this.currentPage
              % endif
              return params
          },

          getFilterParams() {
              let params = {}
              for (var key in this.filters) {
                  var filter = this.filters[key]
                  if (filter.active) {
                      params[key] = filter.value
                      params[key+'.verb'] = filter.verb
                  }
              }
              if (Object.keys(params).length) {
                  params.filter = true
              }
              return params
          },

          getAllParams() {
              return {...this.getBasicParams(),
                      ...this.getFilterParams()}
          },

          ## TODO: i noticed buefy docs show using `async` keyword here,
          ## so now i am too.  knowing nothing at all of if/how this is
          ## supposed to improve anything.  we shall see i guess
          async loadAsyncData(params, success, failure) {

              if (params === undefined || params === null) {
                  params = new URLSearchParams(this.getBasicParams())
                  params.append('partial', true)
                  params = params.toString()
              }

              this.loading = true
              this.$http.get(`${'$'}{this.ajaxDataUrl}?${'$'}{params}`).then(({ data }) => {
                  ${grid.component_studly}CurrentData = data.data
                  this.data = ${grid.component_studly}CurrentData
                  this.rowStatusMap = data.row_status_map
                  this.total = data.total_items
                  this.firstItem = data.first_item
                  this.lastItem = data.last_item
                  this.loading = false
                  this.checkedRows = this.locateCheckedRows(data.checked_rows)
                  if (success) {
                      success()
                  }
              })
              .catch((error) => {
                  this.data = []
                  this.total = 0
                  this.loading = false
                  if (failure) {
                      failure()
                  }
                  throw error
              })
          },

          locateCheckedRows(checked) {
              let rows = []
              if (checked) {
                  for (let i = 0; i < this.data.length; i++) {
                      if (checked.includes(i)) {
                          rows.push(this.data[i])
                      }
                  }
              }
              return rows
          },

          onPageChange(page) {
              this.currentPage = page
              this.loadAsyncData()
          },

          onSort(field, order, event) {

              if (event.ctrlKey) {

                  // engage or enhance multi-column sorting
                  let sorter = this.backendSorters.filter(i => i.field === field)[0]
                  if (sorter) {
                      sorter.order = sorter.order === 'desc' ? 'asc' : 'desc'
                  } else {
                      this.backendSorters.push({field, order})
                  }
                  this.sortingPriority = this.backendSorters

              } else {

                  // sort by single column only
                  this.backendSorters = [{field, order}]
                  this.sortingPriority = []
              }

              // always reset to first page when changing sort options
              // TODO: i mean..right? would we ever not want that?
              this.currentPage = 1
              this.loadAsyncData()
          },

          sortingPriorityRemoved(field) {

              // prune field from active sorters
              this.backendSorters = this.backendSorters.filter(
                  (sorter) => sorter.field !== field)

              // nb. must keep active sorter list "as-is" even if
              // there is only one sorter; buefy seems to expect it
              this.sortingPriority = this.backendSorters

              this.loadAsyncData()
          },

          resetView() {
              this.loading = true

              // use current url proper, plus reset param
              let url = '?reset-to-default-filters=true'

              // add current hash, to preserve that in redirect
              if (location.hash) {
                  url += '&hash=' + location.hash.slice(1)
              }

              location.href = url
          },

          addFilterButton(event) {
              this.addFilterShow = true
              this.$nextTick(() => {
                  this.$refs.addFilterAutocomplete.focus()
              })
          },

          addFilterKeydown(event) {

              // ESC will clear searchbox
              if (event.which == 27) {
                  this.addFilterTerm = ''
                  this.addFilterShow = false
              }
          },

          addFilterSelect(filtr) {
              this.addFilter(filtr.key)
              this.addFilterTerm = ''
              this.addFilterShow = false
          },

          addFilter(filter_key) {

              // show corresponding grid filter
              this.filters[filter_key].visible = true
              this.filters[filter_key].active = true

              // track down the component
              var gridFilter = null
              for (var gf of this.$refs.gridFilters) {
                  if (gf.filter.key == filter_key) {
                      gridFilter = gf
                      break
                  }
              }

              // tell component to focus the value field, ASAP
              this.$nextTick(function() {
                  gridFilter.focusValue()
              })

          },

          applyFilters(params) {
              if (params === undefined) {
                  params = {}
              }

              // merge in actual filter params
              // cf. https://stackoverflow.com/a/171256
              params = {...params, ...this.getFilterParams()}

              // hide inactive filters
              for (var key in this.filters) {
                  var filter = this.filters[key]
                  if (!filter.active) {
                      filter.visible = false
                  }
              }

              // set some explicit params
              params.partial = true
              params.filter = true

              params = new URLSearchParams(params)
              this.loadAsyncData(params)
              this.appliedFiltersHook()
          },

          appliedFiltersHook() {},

          clearFilters() {

              // explicitly deactivate all filters
              for (var key in this.filters) {
                  this.filters[key].active = false
              }

              // then just "apply" as normal
              this.applyFilters()
          },

          // explicitly set filters for the grid, to the given set.
          // this totally overrides whatever might be current.  the
          // new filter set should look like:
          //
          //     [
          //         {key: 'status_code',
          //          verb: 'equal',
          //          value: 1},
          //         {key: 'description',
          //          verb: 'contains',
          //          value: 'whatever'},
          //     ]
          //
          setFilters(newFilters) {
              for (let key in this.filters) {
                  let filter = this.filters[key]
                  let active = false
                  for (let newFilter of newFilters) {
                      if (newFilter.key == key) {
                          active = true
                          filter.active = true
                          filter.visible = true
                          filter.verb = newFilter.verb
                          filter.value = newFilter.value
                          break
                      }
                  }
                  if (!active) {
                      filter.active = false
                      filter.visible = false
                  }
              }
              this.applyFilters()
          },

          saveDefaults() {

              // apply current filters as normal, but add special directive
              this.applyFilters({'save-current-filters-as-defaults': true})
          },

          deleteObject(event) {
              // we let parent component/app deal with this, in whatever way makes sense...
              // TODO: should we ever provide anything besides the URL for this?
              this.$emit('deleteActionClicked', event.target.href)
          },

          checkedRowUUIDs() {
              let uuids = []
              for (let row of this.$data.checkedRows) {
                  uuids.push(row.uuid)
              }
              return uuids
          },

          allRowUUIDs() {
              let uuids = []
              for (let row of this.data) {
                  uuids.push(row.uuid)
              }
              return uuids
          },

          // when a user clicks a row, handle as if they clicked checkbox.
          // note that this method is only used if table is "checkable"
          rowClick(row) {
              let i = this.checkedRows.indexOf(row)
              if (i >= 0) {
                  this.checkedRows.splice(i, 1)
              } else {
                  this.checkedRows.push(row)
              }
              % if grid.check_handler:
              this.${grid.check_handler}(this.checkedRows, row)
              % endif
          },
      }
  }

</script>
