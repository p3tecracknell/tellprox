<div id="rows">
	<h2>Server</h2>
	<div class="row">
		<div class="col-sm-4 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Host that this server will run on">
				<dt><h6>Host</h6></dt>
				<dd><div class="form-group"><input type="text" class="form-control" name="host"></div></dd>
			</dl>
		</div>
		<div class="col-sm-3 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Port that this server will run on">
				<dt><h6>Port</h6></dt>
				<dd><input type="text" name="port"></dd>
			</dl>
		</div>
		<div class="col-sm-5 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Optional root value. Ideal if using Apache forwarding. Requires a restart">
				<dt><h6>Web Root</h6></dt>
				<dd><input type="text" name="webroot"></dd>
			</dl>
		</div>
	</div>
<h2>Client</h2>
	<div class="row">
		<div class="col-sm-4 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="The name of this client when the Web Service publishes information">
				<dt><h6>Client name</h6></dt>
				<dd><input type="text" name="client_name"></dd>
			</dl>
		</div>
		<div class="col-sm-2 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="The ID of this client when the Web Service publishes information">
				<dt><h6>Client ID</h6></dt>
				<dd><input type="text" name="client_id"></dd>
			</dl>
		</div>
		<div class="col-sm-2 col-xs-4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Debug mode enables bottle's debug mode as well as reloads the server on code change">
				<dt><h6>Debug</h6></dt>
				<dd class="make-switch">
					<input type="checkbox" checked="" name="debug" />
				</dd>
			</dl>
		</div>
		<div class="col-sm-2 col-xs-4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h6>Editable</h6></dt>
				<dd class="make-switch">
					<input type="checkbox" checked="" name="editable" />
				</dd>
			</dl>
		</div>
		<div class="col-sm-2 col-xs-4">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="">
				<dt><h6>Pretty Print</h6></dt>
				<dd class="make-switch">
					<input type="checkbox" checked="" name="pretty_print" />
				</dd>
			</dl>
		</div>
	</div>
	<h2>Authentication</h2>
	<div class="row">
		<div class="col-sm-3 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Username for Web Authentication">
				<dt><h6>Username</h6></dt>
				<dd><input type="text" name="username"></dd>
			</dl>
		</div>
		<div class="col-sm-4 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Password for Web Authentication">
				<dt><h6>Password</h6></dt>
				<dd><input type="password" name="password" value=""><span id="removePassword" class="input-icon fui-cross"></span></dd>
			</dl>
		</div>
		<div class="col-sm-5 col-xs-6">
			<dl class="palette palette-alizarin" rel="tooltip" data-original-title="Key used when accessing the API only">
				<dt><h6>API Key</h6></dt>
				<dd><input type="text" name="apikey" value=""></dd>
			</dl>
		</div>
	</div>
</div>
<script>				
	$('input').addClass('form-control');
	$('dd').addClass('form-group');
	$removePassword = $('#removePassword');
			
	$(document).ready(function() {
		api.config.getall(function(configData) {
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
						input.val(val);
						break;
					case 'password':
						input.val(val.length > 0 ? 'notherealone' : '');
					}
				}
				
				input.change(function() {
					var item = input.attr('name'),
						value = getValue(input);
					
					setValue(item, value);
				});
			});
			
			$removePassword.click(onRemovePasswordClick);
		});
	});
	
	function setValue(item, value) {
		api.config.set(item, value, function(data) {
			if ('status' in data && data['status'] == 'success') {
				type = 'success';
				message = '<i>' + item + '</i> set successfully';
			} else {
				type = 'danger';
				message = data['error'] || 'fail';
			}
			createToast(type, message);
		});
	}
	
	function onRemovePasswordClick() {
		$('input[type=password]').val();
		setValue('password', '');
	}
	
	function createToast(type, message){
		$.toast(message, {
			duration: 2500,
			sticky: false,
			type: type
		});
	}
	$('[rel=tooltip]').tooltip({placement: 'bottom'})
</script>
%rebase layout title='Config', name='config', **locals()