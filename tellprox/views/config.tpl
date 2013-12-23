<div id="rows">
	<h2>Server</h2>
	<div class="row-fluid">
		<div class="span4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Host that this server will run on">
				<dt><h4>Host</h4></dt>
				<dd><input type="text" class="span4" name="host"></dd>
			</dl>
		</div>
		<div class="span3">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Port that this server will run on">
				<dt><h4>Port</h4></dt>
				<dd><input type="text" class="span3" name="port"></dd>
			</dl>
		</div>
		<div class="span5">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Optional root value. Ideal if using Apache forwarding">
				<dt><h4>Web Root</h4></dt>
				<dd><input type="text" class="span5" name="webroot"></dd>
			</dl>
		</div>
	</div>
	<h2>Client</h2>
	<div class="row-fluid">
		<div class="span4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="The name of this client when the Web Service publishes information">
				<dt><h4>Client name</h4></dt>
				<dd><input type="text" class="span4" name="client_name"></dd>
			</dl>
		</div>
		<div class="span2">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="The ID of this client when the Web Service publishes information">
				<dt><h4>Client ID</h4></dt>
				<dd><input type="text" class="span2" name="client_id"></dd>
			</dl>
		</div>
		<div class="span2">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Debug mode enables bottle's debug mode as well as reloads the server on code change">
				<dt><h4>Debug</h4></dt>
				<dd class="make-switch">
					<input type="checkbox" checked="" name="debug" />
				</dd>
			</dl>
		</div>
		<div class="span2">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Editable</h4></dt>
				<dd class="make-switch">
					<input type="checkbox" checked="" name="editable" />
				</dd>
			</dl>
		</div>
		<div class="span2">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Pretty Print</h4></dt>
				<dd class="make-switch">
					<input type="checkbox" checked="" name="pretty_print" />
				</dd>
			</dl>
		</div>
	</div>
	<h2>Authentication</h2>
	<div class="row-fluid">
		<div class="span3">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Username</h4></dt>
				<dd><input type="text" class="span3" name="username"></dd>
			</dl>
		</div>
		<div class="span4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>Password</h4></dt>
				<dd><input type="password" class="span4" value="notherealone" name="password" value=""></dd>
			</dl>
		</div>
		<div class="span5">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h4>API Key</h4></dt>
				<dd><input type="text" class="span5" name="apikey" value=""></dd>
			</dl>
		</div>
	</div>
</div>

<!-- Placed at the end of the document so the pages load faster -->
<script src="static/js/jquery-1.8.3.min.js"></script>
<script src="static/js/jquery-ui-1.8.23.custom.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/bootstrap-switch.js"></script>
<script src="static/js/jquery.toast.min.js"></script>
<script src="static/js/helpers.js"></script>
<script>
	var GETALL_URL = 'json/config/getall';
	var SET_URL = 'json/config/set';
	
	$(document).ready(function() {
		$.post(GETALL_URL, authData(), function(configData) {
			$('#rows dl').each(function(i, field) {
				var root = $(field);
				var label = root.find('dt:first >:first-child');
				var input = root.find('input:first');
				input.attr('label', label.text());
				
				var name = input.attr('name');
				if (name in configData) {
					var val = configData[name];
					
					switch(input.attr('type')) {
					case 'checkbox':
						root.bootstrapSwitch('setState', val, true);
						break;
					case 'text':
						if (name != 'password') input.val(val);
						break;
					}
				}
				
				input.change(function() {
					var item = input.attr('name');
					var inputData = authData({ 'item': item, 'value': getValue(input) });
					$.post(SET_URL, inputData, function(data) {
						if ('status' in data && data['status'] == 'success') {
							type = 'success';
							message = '<i>' + input.attr('label') + '</i> set successfully';;
						} else {
							type = 'danger';
							message = data['error'] || 'fail';
						}
						createToast(type, message);
					});
				});
			});
		});
	});
	
	function createToast(type, message){
		$.toast(message, {
			duration: 2500,
			sticky: false,
			type: type
		});
	}
	
	function getValue(input) {
		if (input.attr('type') == 'checkbox')
			return input.is(':checked');
		else
			return input.val();
	}
	$('[rel=tooltip]').tooltip({placement: 'bottom'})
</script>
%rebase layout title='Config', name='config', **locals()