## -*- coding: utf-8; -*-
<%inherit file="/batch/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    % if allow_edit_catalog_unit_cost:
        td.c_catalog_unit_cost {
            cursor: pointer;
            background-color: #fcc;
        }
        tr.catalog_cost_confirmed td.c_catalog_unit_cost {
            background-color: #cfc;
        }
    % endif
    % if allow_edit_invoice_unit_cost:
        td.c_invoice_unit_cost {
            cursor: pointer;
            background-color: #fcc;
        }
        tr.invoice_cost_confirmed td.c_invoice_unit_cost {
            background-color: #cfc;
        }
    % endif
  </style>
</%def>

<%def name="render_po_vs_invoice_helper()">
  % if master.handler.has_purchase_order(batch) and master.handler.has_invoice_file(batch):
      <div class="object-helper">
        <h3>PO vs. Invoice</h3>
        <div class="object-helper-content">
          ${po_vs_invoice_breakdown_grid}
        </div>
      </div>
  % endif
</%def>

<%def name="render_auto_receive_helper()">
  % if master.has_perm('auto_receive') and master.can_auto_receive(batch):

      <div class="object-helper">
        <h3>Tools</h3>
        <div class="object-helper-content">
          <b-button type="is-primary"
                    @click="autoReceiveShowDialog = true"
                    icon-pack="fas"
                    icon-left="check">
            Auto-Receive All Items
          </b-button>
        </div>
      </div>

      <b-modal has-modal-card
               :active.sync="autoReceiveShowDialog">
        <div class="modal-card">

          <header class="modal-card-head">
            <p class="modal-card-title">Auto-Receive All Items</p>
          </header>

          <section class="modal-card-body">
            <p class="block">
              You can automatically set the "received" quantity to
              match the "shipped" quantity for all items, based on
              the invoice.
            </p>
            <p class="block">
              Would you like to do so?
            </p>
          </section>

          <footer class="modal-card-foot">
            <b-button @click="autoReceiveShowDialog = false">
              Cancel
            </b-button>
            ${h.form(url('{}.auto_receive'.format(route_prefix), uuid=batch.uuid), **{'@submit': 'autoReceiveSubmitting = true'})}
            ${h.csrf_token(request)}
            <b-button type="is-primary"
                      native-type="submit"
                      :disabled="autoReceiveSubmitting"
                      icon-pack="fas"
                      icon-left="check">
              {{ autoReceiveSubmitting ? "Working, please wait..." : "Auto-Receive All Items" }}
            </b-button>
            ${h.end_form()}
          </footer>
        </div>
      </b-modal>
  % endif
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}

  % if allow_edit_catalog_unit_cost or allow_edit_invoice_unit_cost:
      <script type="text/x-template" id="receiving-cost-editor-template">
        <div>
          <span v-show="!editing">
            {{ value }}
          </span>
          <b-input v-model="inputValue"
                   ref="input"
                   v-show="editing"
                   size="is-small"
                   @keydown.native="inputKeyDown"
                   @focus="selectAll"
                   @blur="inputBlur"
                   style="width: 6rem;">
          </b-input>
        </div>
      </script>
  % endif
</%def>

<%def name="object_helpers()">
  ${self.render_status_breakdown()}
  ${self.render_po_vs_invoice_helper()}
  ${self.render_execute_helper()}
  ${self.render_auto_receive_helper()}
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.autoReceiveShowDialog = false
    ThisPageData.autoReceiveSubmitting = false

    % if po_vs_invoice_breakdown_data is not Undefined:
        ThisPageData.poVsInvoiceBreakdownData = ${json.dumps(po_vs_invoice_breakdown_data)|n}

        ThisPage.methods.autoFilterPoVsInvoice = function(row) {
            let filters = []
            if (row.key == 'both') {
                filters = [
                    {key: 'po_line_number',
                     verb: 'is_not_null'},
                    {key: 'invoice_line_number',
                     verb: 'is_not_null'},
                ]
            } else if (row.key == 'po_not_invoice') {
                filters = [
                    {key: 'po_line_number',
                     verb: 'is_not_null'},
                    {key: 'invoice_line_number',
                     verb: 'is_null'},
                ]
            } else if (row.key == 'invoice_not_po') {
                filters = [
                    {key: 'po_line_number',
                     verb: 'is_null'},
                    {key: 'invoice_line_number',
                     verb: 'is_not_null'},
                ]
            } else if (row.key == 'neither') {
                filters = [
                    {key: 'po_line_number',
                     verb: 'is_null'},
                    {key: 'invoice_line_number',
                     verb: 'is_null'},
                ]
            }

            if (!filters.length) {
                return
            }

            this.$refs.rowGrid.setFilters(filters)
            document.getElementById('rowGrid').scrollIntoView({
                behavior: 'smooth',
            })
        }

    % endif

    % if allow_edit_catalog_unit_cost or allow_edit_invoice_unit_cost:

        let ReceivingCostEditor = {
            template: '#receiving-cost-editor-template',
            mixins: [SimpleRequestMixin],
            props: {
                row: Object,
                'field': String,
                value: String,
            },
            data() {
                return {
                    inputValue: this.value,
                    editing: false,
                }
            },
            methods: {

                selectAll() {
                    // nb. must traverse into the <b-input> element
                    let trueInput = this.$refs.input.$el.firstChild
                    trueInput.select()
                },

                startEdit() {
                    // nb. must strip $ sign etc. to get the real value
                    let value = this.value.replace(/[^\-\d\.]/g, '')
                    this.inputValue = parseFloat(value) || null
                    this.editing = true
                    this.$nextTick(() => {
                        this.$refs.input.focus()
                    })
                },

                inputKeyDown(event) {

                    // when user presses Enter while editing cost value, submit
                    // value to server for immediate persistence
                    if (event.which == 13) {
                        this.submitEdit()

                    // when user presses Escape, cancel the edit
                    } else if (event.which == 27) {
                        this.cancelEdit()
                    }
                },

                inputBlur(event) {
                    // always assume user meant to cancel
                    this.cancelEdit()
                },

                cancelEdit() {
                    // reset input to discard any user entry
                    this.inputValue = this.value
                    this.editing = false
                    this.$emit('cancel-edit')
                },

                submitEdit() {
                    let url = '${url('{}.update_row_cost'.format(route_prefix), uuid=batch.uuid)}'

                    let params = {
                        row_uuid: this.$props.row.uuid,
                    }
                    params[this.$props.field] = this.inputValue

                    this.simplePOST(url, params, response => {

                        // let parent know cost value has changed
                        // (this in turn will update data in *this*
                        // component, and display will refresh)
                        this.$emit('input', response.data.row[this.$props.field],
                                   this.$props.row._index)

                        // and hide the input box
                        this.editing = false
                    })
                },
            },
        }

        Vue.component('receiving-cost-editor', ReceivingCostEditor)

    % endif

    % if allow_edit_catalog_unit_cost:

        ${rows_grid.component_studly}.methods.catalogUnitCostClicked = function(row) {

            // start edit for clicked cell
            this.$refs['catalogUnitCost_' + row.uuid].startEdit()
        }

        ${rows_grid.component_studly}.methods.catalogCostConfirmed = function(amount, index) {

            // update display to indicate cost was confirmed
            this.addRowClass(index, 'catalog_cost_confirmed')

            // advance to next editable cost input...

            // first try invoice cost within same row
            let thisRow = this.data[index]
            let cost = this.$refs['invoiceUnitCost_' + thisRow.uuid]
            if (!cost) {

                // or, try catalog cost from next row
                let nextRow = this.data[index + 1]
                if (nextRow) {
                    cost = this.$refs['catalogUnitCost_' + nextRow.uuid]
                }
            }

            // start editing next cost if found
            if (cost) {
                cost.startEdit()
            }
        }

    % endif

    % if allow_edit_invoice_unit_cost:

        ${rows_grid.component_studly}.methods.invoiceUnitCostClicked = function(row) {

            // start edit for clicked cell
            this.$refs['invoiceUnitCost_' + row.uuid].startEdit()
        }

        ${rows_grid.component_studly}.methods.invoiceCostConfirmed = function(amount, index) {

            // update display to indicate cost was confirmed
            this.addRowClass(index, 'invoice_cost_confirmed')

            // advance to next editable cost input...

            // nb. always advance to next row, regardless of field
            let nextRow = this.data[index + 1]
            if (nextRow) {

                // first try catalog cost from next row
                let cost = this.$refs['catalogUnitCost_' + nextRow.uuid]
                if (!cost) {

                    // or, try invoice cost from next row
                    cost = this.$refs['invoiceUnitCost_' + nextRow.uuid]
                }

                // start editing next cost if found
                if (cost) {
                    cost.startEdit()
                }
            }
        }

    % endif

  </script>
</%def>


${parent.body()}
