<div id="rows"></div>
<div id="loading"></div>

<script src="static/js/jquery-1.8.3.min.js"></script>
<script src="static/js/jquery-ui-1.8.23.custom.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/bootstrap-switch.js"></script>
<script src="static/js/helpers.js"></script>
<script>
	// URLs
	var URL_BASE = 'json/';
	var DEVICES_URL = URL_BASE + 'devices/list';
	var DEVICE_DIM_URL = URL_BASE + 'device/dim';
	var DEVICE_ON_URL = URL_BASE + 'device/turnOn';
	var DEVICE_OFF_URL = URL_BASE + 'device/turnOff';

	// Constants
	var SLIDER_ID_PREFIX = 'slider-';
	var TOGGLE1_PREFIX = 'toggleOption1-';
	var TOGGLE2_PREFIX = 'toggleOption2-';
	var TOGGLE_PREFIX = 'toggleOption-';
	var ON_OFF = 3;
	var DIM = 16;

	$(document).ready(function() {
		$.ajax({
			url: DEVICES_URL,
			data: authData({ 'supportedMethods': 19}),
			dataType: "jsonp",
			crossDomain: true,
			success: function(data) {
				loadItems(data);
			}
		});
	});
		
	function createItemCell(name) {
		// Create elements
		var item = {
			cell: div().addClass('span4'),
			header: div().addClass('palette palette-peter-river').
				append(h(2).text(name)),
			body: div().addClass('palette palette-belize-hole')
		};

		item.header.appendTo(item.cell);
		item.body.appendTo(item.cell);
		
		return item;
	}
	
	function createSlider(parent, itemId, startValue) {
		var sliderId = SLIDER_ID_PREFIX + itemId;
		var slider = div().attr({id: sliderId}).addClass('ui-slider');
		parent.append(slider);
		slider.slider({
			min: 0,
			max: 255,
			value: startValue,
			orientation: "horizontal",
			range: "min",
			change: function(event, ui) {
				sliderId = $(this).attr('id').substr(SLIDER_ID_PREFIX.length)
				$.post(DEVICE_DIM_URL, authData({id: sliderId, level: ui.value}))
			}
		});
	}
	
	function createToggle(parent, id, state) {
		var isOn = state == "1"
		
		var toggle = div().addClass('switch').attr({id: TOGGLE_PREFIX + id})
			.append(checkbx(isOn));
		
		parent.append(toggle);
		
		toggle['bootstrapSwitch']();
		toggle.on('switch-change', function (e, data) {
			var url = (data.value) ? DEVICE_ON_URL : DEVICE_OFF_URL;
			var itemId = e.target.id.substr(TOGGLE_PREFIX.length);
			$.post(url, authData({id: itemId}));
		});
	}
	
	function loadItems(data) {
		var rowContainer = $('#rows');
		rowContainer.hide();
		
		if ('device' in data) {
			var devices = data['device']
			var itemCount = 0;
			devices.sort(sort_by('name', true, function(a){return a.toUpperCase()}));
			
			// Loop through all items
			$.each(devices, function(i, v) {
				if (itemCount % 3 == 0) {
					// Add row
					currentRow = div().addClass('row-fluid');
					currentRow.appendTo(rowContainer);
				}
				
				// See if it supports dimming
				var dimmable = ((v.methods & DIM) == DIM);
				
				var item = createItemCell(v.name);
				currentRow.append(item.cell);
				
				if (dimmable)
					createSlider(item.body, v.id, v.statevalue)
				//else
				createToggle(item.body, v.id, v.state)
				
				itemCount++;
			});
		} else {
			rowContainer.text('Error: ' + data['error'] || 'Unknown error');
		}

		$('#loading').hide()
		rowContainer.show();
	}
</script>
%rebase layout title='Devices', name='devices', **locals()