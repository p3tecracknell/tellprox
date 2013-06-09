<div id="rows">
	<div class="row-fluid">
		<div class="span3" id="apiList">
		</div>
		<div class="span9">
			<div id="description">
			Welcome to the API Explorer. Here you can test live calls to the API-server.
			</div>
			<div id="apiSpecifics" style="display:none">
			
				<br/>
				
				<form>
				<div id="inputs"></div>
				
				<br/>
				
				<div id="response">			  
					<label class="radio">
						<span class="icons"><span class="first-icon fui-radio-unchecked"></span><span class="second-icon fui-radio-checked"></span></span><input type="radio" name="outputFormat" id="optionsRadios1" value="json" data-toggle="radio">
						JSON
						</label>
						<label class="radio checked">
						<span class="icons"><span class="first-icon fui-radio-unchecked"></span><span class="second-icon fui-radio-checked"></span></span><input type="radio" name="outputFormat" id="optionsRadios2" value="xml" data-toggle="radio" checked="">
						XML
					</label>
					<br/>
					<a href="#" class="btn btn-large btn-primary" onclick="submitApi()">Send</a>
					<a href="#" class="btn btn-large btn-primary" onclick="submitGet()">Get</a>
					<input type="submit" name="g" value="Submit" id="g" />
				</div>
				</form>
				
				<br/>
				
				<code id="output" style="white-space: pre; display: none"></code>
			</div>
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
						  description: '	(optional) A comma-delimited list of extra information to fetch for each returned client. Currently supported fields are: coordinate, suntime, timezone and tzoffset', type: 'text' }
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
	
	$.fn.appendSpan = function(i, item) {
		this.append(div().addClass('span'+i).append(item))
		return this
	}
	
	$('form').submit(function() {
		var inputData = {}
		$.each($(this).serializeArray(), function(i, elem) {
			if (elem.name != 'outputFormat')
				inputData[elem.name] = elem.value
			else
				outputFormat = elem.value
		})
		
		if (selectedMethod) {
			$.post(outputFormat + '/' + selectedMethod, inputData, function(data) {
				if (outputFormat == 'json') {
					data = JSON.stringify(data, null, '\t')
				}
				output.text(data)
				output.show()
			});
		}
	  return false;
	});
	
	function showPage(methodTitle) {
		if (selectedMethod != methodTitle) {
			if (methodTitle in apiMap) {
				var method = apiMap[methodTitle]
				description.text(method.description)
				
				if ('inputs' in method) {
					var inputArray = method.inputs
					for (var i in inputArray) {
						var input = inputArray[i];
						appendInputText(inputs, input.title, input.description);
					}
				}
				
				output.text('')
				$('#apiSpecifics').show()
				selectedMethod = methodTitle;
			}
		}
	}
	
	function appendInputText(parent, title, description) {
		parent.append(
			div().addClass('palette palette-peter-river')
				.append(
					input().attr({name: title, placeholder: title, 'class': 'span6'})
				)
				.append(
					span().text(description)
				)
		)
	}
	
	function collectInputs() {
		var inputSelection = $('#inputs').find('input')
		var output = {}
		for (var i = 0; i < inputSelection.length; i++) {
			input = inputSelection[i];
			output[input.id] = input.value
		}
		return output
	}
	
	function submitApi() {
		if (selectedMethod) {
			$.post('json/' + selectedMethod, collectInputs(), function(data) {
				output.text(JSON.stringify(data, null, '\t'))
				output.show()
			});
		}
	}
	
	function submitGet() {
		var url = 'json/' + selectedMethod;
		if (!getWindow)
			getWindow = window.open(url, '_blank');
		else
			getWindow.location = url;
		getWindow.focus();
	}
	
	$('[rel=tooltip]').tooltip({placement: 'bottom'})
	$("[data-toggle='switch']").wrap('<div class="switch" />');
</script>
%rebase layout title='API', name='api'