<div id="jobsContainer"></div>
<div id="loading"></div>

<script type="text/x-template" class="jobTemplate">
	<div class="col-xs-12 col-sm-6 col-md-4 paletteContainer">
		<div class="palette palette-peter-river dev-box"><h4 class="header">[JOB]</h4></div>
		<div class="palette palette-belize-hole">
			<div class="pagination">
				<ul class="content" style="width: 100%">[CONTENT]</ul>
			</div>
		</div>
	</div>
</script>
<script>

	var JOBTEMPLATE = $( $( "script.jobTemplate" ).html() ),
		$jobsContainer = $('#jobsContainer');

	$(document).ready(function() {
		api.scheduler.joblist(loadItems);
	});
	
	function createJob(job) {
		return JOBTEMPLATE.clone()
			.find('.header')
				.text(job.id)
				.end()
			.find('.content')
				.text(JSON.stringify(job, '', 2))
				//.empty()
				//.append(slider)
				//.data('id', itemId)
				.end();
	}
	
	function loadItems(data) {
		$jobsContainer.hide();
		
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
			var buffer = $.map(jobs, function(job) {
				return createJob(job);
			});
			$jobsContainer.append(buffer);
		} else {
			$jobsContainer.text('Error: ' + data['error'] || 'Unknown error');
		}
		
		//$('.evtBtn').click(onButtonClick);

		$('#loading').hide()
		$jobsContainer.show();
	}
</script>
%rebase layout title='Scheduler', name='scheduler', **locals()