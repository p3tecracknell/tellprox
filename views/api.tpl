<div id="rows">
	<div class="row-fluid">
		<div class="span2" id="apiList"></div>
		<div class="span7">
			<div id="description">
			Welcome to the API Explorer. Here you can test live calls to the API-server.
			</div>
			<div id="apiSpecifics" style="display:none">
			
				<br/>
				
				<form>
				<div id="inputs"></div>
				
				<br/>
				
				<div id="response">			  
					<label class="radio checked">
						<span class="icons"><span class="first-icon fui-radio-unchecked"></span><span class="second-icon fui-radio-checked"></span></span><input type="radio" name="outputFormat" id="optionsRadios1" value="json" data-toggle="radio" checked>
						JSON
					</label>
					<label class="radio">
						<span class="icons"><span class="first-icon fui-radio-unchecked"></span><span class="second-icon fui-radio-checked"></span></span><input type="radio" name="outputFormat" id="optionsRadios2" value="xml" data-toggle="radio">
						XML
					</label>
					<br/>
					<input type="submit" class="btn btn-large btn-primary" name="post" value="Post" id="post" />
					<input type="submit" class="btn btn-large btn-primary" name="get" value="Get" id="get" />
				</div>
				</form>
				
				<br/>
				
				<code id="output" style="white-space: pre; display: none"></code>
			</div>
		</div>
		<div class="span3" id="itemList">
		<h4>Clients</h4>
		399371 - newname
		</div>
	</div>

<!-- Placed at the end of the document so the pages load faster -->
<script src="static/js/jquery-1.8.3.min.js"></script>
<script src="static/js/jquery-ui-1.8.23.custom.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/bootstrap-switch.js"></script>
<script src="static/js/flatui-radio.js"></script>
<script src="static/js/helpers.js"></script>
<script>
	data =
	[
		{
			title : 'Clients',
			items : [
				{
					title: 'clients/list',
					description: 'Returns a list of all clients associated with the current user.'
				}
			]
		},
		{
			title : 'Client',
			items : [
				{
					title: 'client/info',
					description: 'Returns information about a specific client.',
					inputs: [
						{ title: 'id', description: 'The id of the client', type: 'text' },
						{ title: 'uuid',
						  description: '(optional) An optional uuid for a client. By specifying the uuid, info about a non registered client can be fetched', type: 'text' },
						{ title: 'code',
						  description: '(optional) Not used. Included for backwards compatibility with TellStick Net only', type: 'text' },
						{ title: 'extras',
						  description: '(optional) A comma-delimited list of extra information to fetch for each returned client. Currently supported fields are: coordinate, suntime, timezone and tzoffset', type: 'text' }
					]
				}
			]
		},
		{
			title : 'Devices',
			items : [
				{
					title: 'devices/list',
					description: 'Returns a list of all devices associated with the current user.',
					inputs: [
						{ title: 'supportedMethods', description: 'The methods supported by the calling application', type: 'text' },
						{ title: 'extras', description: '(optional) A comma-delimited list of extra information to fetch for each returned device. Currently supported fields are: coordinate, timezone and tzoffset.', type: 'text' }
					]
				}
			]
		},
		{
			title : 'Device',
			items : [
				{
					title: 'device/toggle',
					description: 'Toggles a device on or off',
					inputs: [
						{ title: 'id', description: 'The device id to toggle', type: 'text' }
					]
				}
			]
		}
	]
	
	var apiMap = {};
	var selectedMethod;
	
	var apiList = $('#apiList');
	var description = $('#description');
	var inputs = $('#inputs');
	var output = $('#output');
	var getWindow;
		
	$(document).ready(function() {
		for(var i in data) {
			var header = data[i];
			apiList.append(h(4).text(header.title))
			var items = header.items
			for (var j in items) {
				var method = items[j]
				var methodTitle = method.title
				apiList.append(a()
					.text(methodTitle)
					.attr({href: '#' + methodTitle})
					.addClass('method')
					.click(function(e) {
						showPage(e.target.text)
					}))
					
				apiMap[methodTitle] = method
			}
		}
		
		if (document.URL.indexOf('#') > 0) {
			var hash = document.URL.substr(document.URL.indexOf('#') + 1)
			showPage(hash)
		}
	});
	
	$("form input[type=submit]").click(function() {
		$("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
		$(this).attr("clicked", "true");
	});
	
	$('form').submit(function(a) {
		var inputData = {};
		$.each($(this).serializeArray(), function(i, elem) {
			if (elem.name != 'outputFormat')
				inputData[elem.name] = elem.value
			else
				outputFormat = elem.value
		});
		
		var url = outputFormat + '/' + selectedMethod;
		var buttonPressed = $("input[type=submit][clicked=true]").val();
		if (buttonPressed == 'Post') {
			$.post(url, inputData, function(data) {
				if (outputFormat == 'json') {
					data = JSON.stringify(data, null, '\t')
				}
				output.text(data)
				output.show()
			});
		} else {
			url += '?' + $.param(inputData);
			getWindow = window.open(url, '_blank');
			getWindow.focus();
		}
	    return false;
	});
	
	function submitGet() {
		var url = 'json/' + selectedMethod;
		if (!getWindow)
			getWindow = window.open(url, '_blank');
		else
			getWindow.location = url;
		getWindow.focus();
	}
	
	function showPage(methodTitle) {
		if (selectedMethod != methodTitle) {
			if (methodTitle in apiMap) {
				var method = apiMap[methodTitle]
				description.text(method.description)
				
				// Clear out, ready to start again
				inputs.empty();
				if ('inputs' in method) {
					var inputArray = method.inputs
					for (var i in inputArray) {
						var input = inputArray[i];
						inputs.append(createInputField(input.title, input.description));
					}
				}
				
				output.text('')
				$('#apiSpecifics').show()
				selectedMethod = methodTitle;
			}
		}
	}
	
	function createInputField(title, description) {
		return div().addClass('palette palette-peter-river')
			.append(input().attr({name: title, placeholder: title, 'class': 'span6'}))
			.append(span().text(description))
	}
	
	/*function collectInputs() {
		var inputSelection = $('#inputs').find('input')
		var output = {}
		for (var i = 0; i < inputSelection.length; i++) {
			input = inputSelection[i];
			output[input.id] = input.value
		}
		return output
	}
	
	//$.fn.appendSpan = function(i, item) {
	//	this.append(div().addClass('span'+i).append(item))
	//	return this
	//}
	
	
	function submitApi() {
		if (selectedMethod) {
			$.post('json/' + selectedMethod, collectInputs(), function(data) {
				output.text(JSON.stringify(data, null, '\t'))
				output.show()
			});
		}
	}
	
	$('[rel=tooltip]').tooltip({placement: 'bottom'})
	$("[data-toggle='switch']").wrap('<div class="switch" />');*/
</script>
%rebase layout title='API', name='api'