## -*- coding: utf-8; -*-

## TODO: deprecate / remove this
## (tried to add deprecation warning here but it didn't seem to work)
<%def name="render_buefy_field(field, bfield_kwargs={})">
  ${form.render_buefy_field(field.name, bfield_attrs=bfield_kwargs)}
</%def>
