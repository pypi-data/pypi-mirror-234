## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">changes @ ver ${transaction.id}</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .this-page-content {
        overflow: auto;
    }

    .versions-wrapper {
        margin-left: 2rem;
    }

  </style>
</%def>

<%def name="page_content()">
## TODO: this was basically copied from Revel diff template..need to abstract

<div class="form-wrapper">

  <div class="form">

    <div class="field-wrapper">
      <label>Changed</label>
      <div class="field">${h.pretty_datetime(request.rattail_config, changed)}</div>
    </div>

    <div class="field-wrapper">
      <label>Changed by</label>
      <div class="field">${transaction.user or ''}</div>
    </div>

    <div class="field-wrapper">
      <label>IP Address</label>
      <div class="field">${transaction.remote_addr}</div>
    </div>

    <div class="field-wrapper">
      <label>Comment</label>
      <div class="field">${transaction.meta.get('comment') or ''}</div>
    </div>

    <div class="field-wrapper">
      <label>TXN ID</label>
      <div class="field">${transaction.id}</div>
    </div>

  </div>

</div><!-- form-wrapper -->

<div class="versions-wrapper">
  % for diff in version_diffs:
      <h4 class="is-size-4 block">${diff.title}</h4>
      ${diff.render_html()}
  % endfor
</div>

</%def>


${parent.body()}
