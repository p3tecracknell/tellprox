<div id="deviceContainer" class="row"></div>
<div id="loading"></div>

<script type="text/x-template" class="itemCellTemplate2">
	<div class="col-xs-12 col-sm-6 col-md-4 paletteContainer">
		<div class="palette palette-peter-river dev-box"><h4 class="header">[DEVICE]</h4></div>
		<div class="palette palette-belize-hole">
			<div class="pagination">
				<ul class="content" style="width: 100%">[CONTENT]</ul>
			</div>
		</div>
	</div>
</script>
<script type="text/x-template" class="itemCellTemplate">
	<div class="col-xs-12 col-sm-6 col-md-4 device-container">
		<div class="device-box"><h4 class="header">[DEVICE]</h4></div>
		<div class="device-controls">
			<div class="pagination">
				<ul class="content" style="width: 100%">[CONTENT]</ul>
			</div>
		</div>
	</div>
</script>
<script type="text/x-template" class="actionButtonTemplate">
	<li style="text-align: center; width: 50%">
		<a href="#" class="evtBtn">[PCG]</a>
	</li>
</script>
<script>
	// Constants
	var ON_OFF = 3,
		DIM = 16;
		
	var NUM_SLIDES = 6,
		SLIDE_WIDTH = 100 / NUM_SLIDES,
		ITEMCELLTEMPLATE = $( $( "script.itemCellTemplate" ).html() ),
		ACTIONBUTTONTEMPLATE = $( $( "script.actionButtonTemplate" ).html() );
		
	var $deviceContainer = $('#deviceContainer');

	$(document).ready(function() {
		api.devices.list(ON_OFF + DIM, loadItems);
	});
	
	function createItemCell(itemId, name, slider) {
		return ITEMCELLTEMPLATE.clone()
			.find('.header')
				.text(name)
				.end()
			.find('.content')
				.empty()
				.append(slider)
				.data('id', itemId)
				.end();
	}
	
	function createSlideButtons(startValue) {
		var buffer = [];
		var currentVal = startValue / 255 * (NUM_SLIDES - 1);
		for (var val = 0; val < NUM_SLIDES; val++) {
			var dataValue =	(val == 0) ? 'off' :
				Math.round(255 * val / (NUM_SLIDES - 1));

			var textValue = Math.round(100 * val / (NUM_SLIDES - 1));
			var anchor = ACTIONBUTTONTEMPLATE.clone()
				.width(SLIDE_WIDTH + '%')
				.find('a')
					.text(textValue + '%')
					.data('val', dataValue)
					.end()
			if (val == currentVal) anchor.addClass('active');
			buffer.push(anchor);
		}
		return buffer;
	}
	
	function createOnOffButton(text, data) {
		return ACTIONBUTTONTEMPLATE.clone()
			.find('a')
				.text(text)
				.data('val', data)
				.end();
	}
	
	function createOnOffButtons(state) {
		var offButton = createOnOffButton('Off', 'off'),
			onButton = createOnOffButton('On', 'on'),
			isOn = (state == '1');
			
		((isOn) ? onButton : offButton).addClass('active');
		return [offButton, onButton];
	}
	
	function onButtonClick(e) {
		var $this = $(this),
			container = $this.parent().parent(),
			id = container.data('id'),
			val = $this.data('val');
		
		e.preventDefault();
		switch(val) {
			case 'on'	: api.device.turnon(id);	break;
			case 'off'	: api.device.turnoff(id);	break;
			default		: api.device.dim(id, val);	break;
		}

		container.children().removeClass('active');
		$this.parent().addClass('active');
	}

	function loadItems(data) {
		$deviceContainer.hide();
		
		if ('device' in data) {
			var devices = data.device;
			devices.sort(sort_by('name', true, function(a){ return a.toUpperCase() }));
			
			// Loop through all items
			var buffer = $.map(devices, function(device) {
				// See if it supports dimming
				var dimmable = ((device.methods & DIM) == DIM),
					controls = (dimmable) ? createSlideButtons(device.statevalue) : createOnOffButtons(device.state);
				
				return createItemCell(device.id, device.name, controls);
			});
			$deviceContainer.append(buffer);
		} else {
			$deviceContainer.text('Error: ' + data['error'] || 'Unknown error');
		}
		
		$('.evtBtn').click(onButtonClick);

		$('#loading').hide()
		$deviceContainer.show();
	}
</script>
%rebase('layout', title='Devices', name='devices', **locals())