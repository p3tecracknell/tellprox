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
		
	var NUM_SLIDES = 6;
	var SLIDE_WIDTH = 100 / NUM_SLIDES;

	$(document).ready(function() {
		$.ajax({
			url: DEVICES_URL,
			data: authData({ 'supportedMethods': ON_OFF + DIM}),
			dataType: "jsonp",
			crossDomain: true,
			success: function(data) {
				loadItems(data);
			}
		});
	});
		
	function createItemCell(name, itemId, startValue, dimmable, state) {
		// Create elements
		var cell = div().addClass('col-xs-12 col-sm-6 col-md-4 paletteContainer'),
			header = div().addClass('palette palette-peter-river dev-box').append(h(4).text(name)),
			contentPalette = div().addClass('palette palette-belize-hole'),
			content = div().addClass('content pagination'),
			slider = createSlider(itemId, startValue, dimmable, state)
			
		contentPalette.append(content);			
		content.append(slider);
		return cell.append(header).append(contentPalette);
	}
	
	function createSlider(itemId, startValue, dimmable, state) {
		var ulEl = ul().width('100%').data('id', itemId);
		if (dimmable) {
			var currentVal = startValue / 255 * (NUM_SLIDES - 1);
			for (var val = 0; val < NUM_SLIDES; val ++) {
				var postVal = Math.round(255 * val / (NUM_SLIDES - 1));
				postVal = (postVal == 0) ? 'off' : postVal;
				var pcg = Math.round(100 * val / (NUM_SLIDES - 1));
				var anchor = a().attr({href:'#'}).text(pcg + '%').addClass('evtBtn').data('val', postVal);
				b = li().css({'text-align': 'center'}).width(SLIDE_WIDTH+'%').append(anchor);
				if (val == currentVal) b.addClass('active');
				ulEl.append(b);
			}
		} else {
			var isOn = state == "1"
			var anchor = a().text('Off').addClass('evtBtn').data('val', 'off');
			bOff = li().css({'text-align': 'right'}).width('50%').append(anchor);
			ulEl.append(bOff);
			
			var anchor = a().text('On').addClass('evtBtn').data('val', 'on');
			bOn = li().css({'text-align': 'left'}).width('50%').append(anchor);
			ulEl.append(bOn);
			
			if (isOn) {
				bOn.addClass('active');
			} else {
				bOff.addClass('active');
			}
		}
		
		return ulEl;
	}

	function loadItems(data) {
		var rowContainer = $('#rows');
		rowContainer.hide();
		
		if ('device' in data) {
			var devices = data.device;
			devices.sort(sort_by('name', true, function(a){ return a.toUpperCase() }));
			
			// Loop through all items
			$.each(devices, function(i, v) {
				// See if it supports dimming
				var dimmable = ((v.methods & DIM) == DIM),
					item = createItemCell(v.name, v.id, v.statevalue, dimmable, v.state);
				
				rowContainer.append(item);
			});
		} else {
			rowContainer.text('Error: ' + data['error'] || 'Unknown error');
		}
		
		$('.evtBtn').click(function(e) {
			e.preventDefault();
			var $this = $(this);
			var ul = $this.parent().parent();
			var id = ul.data('id');
			var val = $this.data('val');
			if (val == 'on') {
				url = DEVICE_ON_URL;
			} else if (val == 'off') {
				url = DEVICE_OFF_URL;
			} else {
				url = DEVICE_DIM_URL;
			}
			
			ul.children().removeClass('active');
			$this.parent().addClass('active');
			$.post(url, authData({id: id, level: val}));
		});

		$('#loading').hide()
		rowContainer.show();
	}
</script>
%rebase layout title='Devices', name='devices', **locals()