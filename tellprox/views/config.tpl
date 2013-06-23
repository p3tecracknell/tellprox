<div id="rows">
	<div class="row-fluid">
		<div class="span6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Host that this server will run on">
				<dt><h4>Host</h4></dt>
				<dd><input type="text" placeholder="Inactive"></dd>
			</dl>
		</div>
		<div class="span6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Port that this server will run on">
				<dt><h4>Port</h4></dt>
				<dd><input type="text" placeholder="Inactive"></dd>
			</dl>
		</div>
	</div>
	<div class="row-fluid">
		<div class="span6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Client name</h4></dt>
				<dd><input type="text" placeholder="Inactive"></dd>
			</dl>
		</div>
		<div class="span6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Client ID</h4></dt>
				<dd><input type="text" placeholder="Inactive"></dd>
			</dl>
		</div>
	</div>
	<div class="row-fluid">
		<div class="span4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Debug</h4></dt>
				<dd class="switch">
					<input type="checkbox" checked="" />
				</dd>
			</dl>
		</div>
		<div class="span4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Editable</h4></dt>
				<dd class="switch">
					<input type="checkbox" checked="" />
				</dd>
			</dl>
		</div>
		<div class="span4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Pretty Print</h4></dt>
				<dd class="switch">
					<input type="checkbox" checked="" />
				</dd>
			</dl>
		</div>
	</div>
</div>

<!-- Placed at the end of the document so the pages load faster -->
<script src="static/js/jquery-1.8.3.min.js"></script>
<script src="static/js/jquery-ui-1.8.23.custom.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/bootstrap-switch.js"></script>
<script src="static/js/helpers.js"></script>
<script>
	$('[rel=tooltip]').tooltip({placement: 'bottom'})
</script>
%rebase layout title='Config', name='config', **locals()