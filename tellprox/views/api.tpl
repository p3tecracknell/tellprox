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
				
				
				<div class="palette palette-peter-river" style="overflow: auto; overflow-y: hidden;">
					<code id="output" style="display:block; white-space:pre; color: #000; background-color: #f7f7f9; border-width: 0">Output
					</code>
				</div>
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
	var API_URL = 'json/api/list';

	data =
	[
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
			title: 'Group',
			items : [
				{
					title: 'group/remove',
					inputs: [
						{ title: 'id', description: 'The device id', type: 'text' }
					]
				}
			]
		},
		{
			title: 'Config',
			items : [
				{
					title: 'config/set',
					inputs: [
						{ title: 'item', type: 'text' },
						{ title: 'value', type: 'text' }
					]
				},
				{
					title: 'config/get',
					inputs: [
						{ title: 'item', type: 'text' }
					]
				},
				{
					title: 'config/getall'
				},
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
	
	$(window).bind('hashchange', showPage);
	$(document).ready(function() {
		$.post(API_URL, authData(), function(groups) {
			apiMap = groups;
			
			for(var header in groups) {
				apiList.append(h(4).text(header))
				for (var methodName in groups[header]) {
					apiList.append(
						a()
						.text(methodName)
						.attr({href: '#' + header + '/' + methodName})
						.addClass('method')
					)
					.append(br());
				}
			}
			
			if (document.URL.indexOf('#') > 0) showPage();
		});
	});
	
	$('form input[type=submit]').click(function() {
		$('input[type=submit]', $(this).parents('form')).removeAttr("clicked");
		$(this).attr('clicked', 'true');
	});
	
	$('form').submit(function(a) {
		var inputData = authData();
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
				} else {
					data = (new window.XMLSerializer()).serializeToString(data);
				}
				output.text(data)
			}).fail(function(o, title, error) { 
				output.text(error);
			});
		} else {
			url += '?' + $.param(inputData);
			getWindow = window.open(url, '_blank');
			getWindow.focus();
		}
	    return false;
	});
	
	function showPage() {
		var title = document.URL.substr(document.URL.indexOf('#') + 1);

		if (selectedMethod != title) {
			var split = title.split('/');
			var groupName = split[0];
			var methodName = split[1];
			if (groupName in apiMap) {
				var group = apiMap[groupName];
				if (methodName in group) {
					var method = group[methodName];
					description.text(method.description || '[Description needed]');

					// Clear out, ready to start again
					inputs.empty();
					if ('inputs' in method) {
						var inputArray = method.inputs
						for (var i in inputArray) {
							var input = inputArray[i];
							switch (input.type) {
								case 'string':
								case 'int':
									inputs.append(createInputField(input.name, input.description));
									break;
								default:
									console.log('todo')
									break;
							}
						}
					}
					
					output.text('')
					$('#apiSpecifics').show()
					selectedMethod = title;
				}
			}
		}
	}
	
	function createInputField(title, description) {
		return div().addClass('palette palette-peter-river')
			.append(input().attr({name: title, placeholder: title, 'class': 'span6'}))
			.append(span().text(description))
	}
</script>
%rebase layout title='API', name='api', **locals()