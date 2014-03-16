<div id="deviceContainer"></div>
<div id="loading"></div>

<script type="text/x-template" class="itemCellTemplate">
	<div class="col-xs-12 col-sm-6 col-md-4 paletteContainer">
		<div class="palette palette-peter-river dev-box"><h4 class="header">[JOB]</h4></div>
		<div class="palette palette-belize-hole">
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
	var ON_OFF = 3,
		DIM = 16;
		
	var NUM_SLIDES = 6,
		SLIDE_WIDTH = 100 / NUM_SLIDES,
		ITEMCELLTEMPLATE = $( $( "script.itemCellTemplate" ).html() ),
		ACTIONBUTTONTEMPLATE = $( $( "script.actionButtonTemplate" ).html() );
		
	var $deviceContainer = $('#deviceContainer');

	$(document).ready(function() {
		api.scheduler.joblist(loadItems);
	});
	
	function createItemCell(itemId, name, slider) {
		return ITEMCELLTEMPLATE.clone()
			.find('.header')
				//.text(name)
				.end()
			.find('.content')
				//.empty()
				//.append(slider)
				//.data('id', itemId)
				.end();
	}
	
	function loadItems(data) {
		$deviceContainer.hide();
		
		if ('job' in data) {
			var jobs = data.job;
			var groupedJobs = {};
			$.each(jobs, function(i, job) {
				var key = job.deviceId;
				if (!groupedJobs[key]) groupedJobs[key] = []
				groupedJobs[key].push(job);
			});
			//jobs.sort(sort_by('name', true, function(a){ return a.toUpperCase() }));
			
			// Loop through all items
			var buffer = $.map(jobs, function(device) {
				// See if it supports dimming
				//var dimmable = ((device.methods & DIM) == DIM),
					//controls = (dimmable) ? createSlideButtons(device.statevalue) : createOnOffButtons(device.state);
				
				return createItemCell();//device.id, device.name, null);
			});
			$deviceContainer.append(buffer);
		} else {
			$deviceContainer.text('Error: ' + data['error'] || 'Unknown error');
		}
		
		//$('.evtBtn').click(onButtonClick);

		$('#loading').hide()
		$deviceContainer.show();
	}
</script>
%rebase layout title='Scheduler', name='scheduler', **locals()