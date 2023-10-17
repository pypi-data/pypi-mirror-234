## -*- coding: utf-8; -*-

<form action="${form.action_url}" method="GET" @submit.prevent="applyFilters()">

  <grid-filter v-for="key in filtersSequence"
               :key="key"
               :filter="filters[key]"
               ref="gridFilters">
  </grid-filter>

  <b-field grouped>

    <b-button type="is-primary"
              native-type="submit"
              icon-pack="fas"
              icon-left="check"
              class="control">
      Apply Filters
    </b-button>

    <b-button v-if="!addFilterShow"
              icon-pack="fas"
              icon-left="plus"
              class="control"
              @click="addFilterButton">
      Add Filter
    </b-button>

    <b-autocomplete v-if="addFilterShow"
                    ref="addFilterAutocomplete"
                    :data="addFilterChoices"
                    v-model="addFilterTerm"
                    placeholder="Add Filter"
                    field="key"
                    :custom-formatter="filtr => filtr.label"
                    open-on-focus
                    keep-first
                    icon-pack="fas"
                    clearable
                    clear-on-select
                    @select="addFilterSelect"
                    @keydown.native="addFilterKeydown">
    </b-autocomplete>

    <b-button @click="resetView()"
              icon-pack="fas"
              icon-left="home"
              class="control">
      Default View
    </b-button>

    <b-button @click="clearFilters()"
              icon-pack="fas"
              icon-left="trash"
              class="control">
      No Filters
    </b-button>

    % if allow_save_defaults and request.user:
        <b-button @click="saveDefaults()"
                  icon-pack="fas"
                  icon-left="save"
                  class="control">
          Save Defaults
        </b-button>
    % endif

  </b-field>

</form>
