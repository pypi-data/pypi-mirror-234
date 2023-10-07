## -*- coding: utf-8; -*-
<%inherit file="/batch/create.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ${form.component_studly}Data.parsers = ${json.dumps(parsers_data)|n}

    ${form.component_studly}Data.vendorName = null
    ${form.component_studly}Data.vendorNameReplacement = null

    ${form.component_studly}.watch.field_model_parser_key = function(val) {
        let parser = this.parsers[val]
        if (parser.vendor_uuid) {
            if (this.field_model_vendor_uuid != parser.vendor_uuid) {
                // this.field_model_vendor_uuid = parser.vendor_uuid
                // this.vendorName = parser.vendor_name
                this.$refs.vendorAutocomplete.setSelection({
                    value: parser.vendor_uuid,
                    label: parser.vendor_name,
                })
            }
        }
    }

    ${form.component_studly}.methods.vendorLabelChanging = function(label) {
        this.vendorNameReplacement = label
    }

    ${form.component_studly}.methods.vendorChanged = function(uuid) {
        if (uuid) {
            this.vendorName = this.vendorNameReplacement
            this.vendorNameReplacement = null
        }
    }

  </script>
</%def>


${parent.body()}
