<div class="row">
	<div class="col-md-3 col-xs-6">
		<select id="groups" class="select-block"></select>
	</div>
	<div class="col-md-3 col-xs-6">
		<select id="methods" class="select-block"></select>
	</div>
</div>

<div id="description"></div>

<form>
	<div id="inputs"></div>
	<br/>
	<div class="row">
		<div class="col-md-3 col-xs-4">
			<select id="outputFormat" name="outputFormat" class="select-block">
				<optgroup label="Output Format">
					<option value="json"
					%if outputFormat == 'json':
						selected
					%end
					>JSON</option>
					<option value="xml"
					%if outputFormat == 'xml':
						selected
					%end
					>XML</option>
				</optgroup>
			</select>
		</div>
		<div class="col-md-3 col-xs-4">
			<input type="submit" class="btn btn-large btn-inverse btn-block" name="post" value="Post" id="post" />
		</div>
		<div class="col-md-3 col-xs-4">
			<input type="submit" class="btn btn-large btn-inverse btn-block" name="get" value="Get" id="get" />
		</div>
	</div>
</form>

<br/>

<div class="palette palette-peter-river" style="overflow: auto; overflow-y: hidden;">
	<code id="postOutput">Output</code>
</div>

<script type="text/x-template" class="inputTemplate">
	<div class="palette palette-peter-river">
		<div class="input"></div>
		<div class="description"></div>
	</div>
</script>
<script>	
	var apiMap,
		selectedMethod,
		getWindow,
		description = $('#description'),
		inputTemplate = $( $( "script.inputTemplate" ).html() ),
		inputs = $('#inputs'),
		output = $('#postOutput'),
		$groups = $('#groups'),
		$methods = $('#methods'),
		$outputFormat = $('#outputFormat');
	
	$(document).ready(function() {
		api.api.list(function(groups) {
			apiMap = groups;
			
			var buffer = mapSorted(apiMap, function(key) {
				return option(key, key);
			});
			$groups.append(buffer);
			
			$(window).bind('hashchange', showPage);
			$groups.change(onGroupChange);
			$methods.change(onMethodChange);
			$outputFormat.change(onOutputFormatChange);
			
			$('select').selectpicker({style: 'btn-primary'});
			
			if (window.location.hash) {
				var hash = getHash().split('/');
				if (hash.length == 2) {
					var group = hash[0],
						method = hash[1];
					setDropdownFromText($groups, group);
					setDropdownFromText($methods, method);
					showPage();
					return;
				}
			}
				
			selectFirstDropdown($groups);
		});
	});
	
	function onOutputFormatChange() {
		api.config.set('outputFormat', $(this).val());
	}
	
	function onGroupChange() {
		var groupName = $(this).val(),
			group = apiMap[groupName];

		$methods.find('option').remove();

		var buffer = mapSorted(group, function(key, value) {
			return option(key, groupName + '/' + key);
		});
		$methods.append(buffer).selectpicker('render');
		
		selectFirstDropdown($methods);
	}
	
	function onMethodChange() {
		var method = $(this).val();
		window.location.hash = method;
	}
	
	$('form input[type=submit]').click(function() {
		$('input[type=submit]', $(this).parents('form')).removeAttr("clicked");
		$(this).attr('clicked', 'true');
	});
	
	$('form').submit(function(a) {
		// Duplicate authdata as we do not want to modify it
		var inputData = $.extend({}, api.getAuthData()),
			pre;
		
		// Combine all the inputs. Comma seperate multiple selects
		$.each($(this).serializeArray(), function(i, elem) {
			pre = (inputData[elem.name]) ? inputData[elem.name] + ',' : '';
			inputData[elem.name] = pre + elem.value
		})
		
		var outputFormat = inputData['outputFormat'];
		delete inputData['outputFormat'];
		
		var url = (outputFormat + '/' + selectedMethod).toLowerCase();
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
		var title = getHash();

		if (selectedMethod != title) {
			var split = title.split('/'),
				groupName = split[0],
				methodName = split[1];

			if (groupName in apiMap) {
				var group = apiMap[groupName];
				if (methodName in group) {
					var method = group[methodName];
					description.text(method.description || '[Description needed]');

					// Clear out, ready to start again
					inputs.empty();
					if ('inputs' in method) {
						var newInput;
						var buffer = $.map(method.inputs, function(input) {
							switch (input.type) {
								case 'string':
								case 'int':
									newInput = inputtext();
									break;
								case 'dropdown':
									newInput = dropdown(input.options);
									break;
								case 'dropdown-multiple':
									newInput = dropdown(input.options).attr('multiple','multiple');
									break;
								default:
									console.log('todo');
									newInput = null;
									break;
							}
							if (newInput) {
								return createInput(input.name, input.description, newInput)
							}
						});
						inputs.append(buffer);
						//inputs.find('select').selectpicker({style: 'btn-primary'})
					}
					
					output.text('');
					selectedMethod = title;
				}
			}
		}
	}
	
	function createInput(title, description, input) {
		input.attr({
			name:			title,
			placeholder:	title,
			'class':		'form-control'
		});
		return inputTemplate.clone()
			.find('.description')
				.text(description)
				.end()
			.find('.input')
				.replaceWith(input)
				.end();
	}
</script>
%rebase('layout', title='API', name='api', **locals())