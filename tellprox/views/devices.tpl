<div id="deviceContainer" class="row" data-bind="foreach: { data: devices, beforeRemove: removeDeviceBox }">
	<div class="col-xs-12 col-sm-6 col-md-4 device-container">
		<div class="device-box">
			<h4 class="header" data-bind="text: name"></h4>
			<a href="#" class="config" data-bind="click: $parent.selectedDevice">
				<span class="device-config"></span>
			</a>
		</div>
		<div class="device-controls">
			<div class="pagination">
				<ul class="content" style="width: 100%" data-bind="slideButtons: dimmable">
					<!-- ko ifnot: dimmable -->
						<li style="text-align: center; width: 50%" data-bind="css: {active: state() == 1}">
							<a href="#" class="evtBtn" data-bind="click: setOn">On</a>
						</li><li style="text-align: center; width: 50%" data-bind="css: {active: state() != 1}">
							<a href="#" class="evtBtn" data-bind="click: setOff">Off</a>
						</li>
					<!-- /ko -->
				</ul>
			</div>
		</div>
	</div>
</div>
<div id="loading"></div>
<div id="lightbox">
	<div id="deviceEditor" data-bind="with: selectedDevice">
		!!Work in Progress!!
		<span data-bind="text: name"></span>
		<button data-bind="click: $parent.removeDevice">Remove</button>
		<!--button data-bind="click: addDevice">Add</button-->
		
	</div>
</div>

<script type="text/x-template" class="actionButtonTemplate">
	<li style="text-align: center;" data-bind="css: {active: isActive($element)}">
		<a href="#" class="evtBtn" data-bind="click: setDim">[PCG]</a>
	</li>
</script>
<script>
	var devicesViewModel;
	
	// Constants
	var OFF = 0,
		ON  = 1,
		DIM = 16,
		ON_OFF = OFF + ON,
		SUPPORTED_METHODS = ON_OFF + DIM;
		
	var NUM_SLIDES = 6,
		SLIDE_WIDTH = 100 / NUM_SLIDES,
		ACTIONBUTTONTEMPLATE = $( $( "script.actionButtonTemplate" ).html() );
		
	var $deviceContainer = $('#deviceContainer'),
		$lightbox = $('#lightbox');
	
	function DeviceViewModel(device) {
		var me = this;
		
		this.id          = device.id;
		this.name        = ko.observable(device.name);
		this.methods     = ko.observable(device.methods);
		this._state      = ko.observable(device.state);
		this._statevalue = ko.observable(device.statevalue);
		
		this.state = ko.computed({
			read:  function()  { return this._state(); },
			write: function(val) {
				this._state(val);
				if (val == ON) api.device.turnon(this.id);
				else		   api.device.turnoff(this.id);
			}
		}, this);
		
		this.statevalue = ko.computed({
			read:  function()  { return Math.round(this._statevalue() / 255 * (NUM_SLIDES - 1)); },
			write: function(val) {
				var val = Math.round(255 * val / (NUM_SLIDES - 1));
				this._statevalue(val);
				if (val == 0) api.device.turnoff(this.id);
				else		  api.device.dim(this.id, val);
			}
		}, this);
		
		this.setOn  = function() { this.state(ON); }
		this.setOff = function() { this.state(OFF); }
		this.setDim = function(v, e) {
			var parent = $(e.currentTarget).parent();
			this.statevalue(parent.data('val'));
		};
		
		this.dimmable = ko.computed(function() {
			return ((this.methods() & DIM) == DIM);
		}, this);
		
		this.isActive = function(element) {
			var position = $(element).data('val'),
				currentVal = this.statevalue();
			return currentVal == position;
		}.bind(this);
			
		// TODO use mapping plugin
		this.update = function(device) {
			this.name(device.name);
			this.methods(device.methods);
			if ('model' in device) {
				this.model = device.model;
			}
		};
	}
	
	function DevicesViewModel(data) {
		var me = this;
		
		var devices = $.map(data, function(device) {
			return new DeviceViewModel(device);
		});
		this.devices = ko.observableArray(devices);
		
		this.removeDevice = function() {
			me.selectedDevice(false);
			me.devices.remove(this);
			api.device.remove(this.id);
		}
		
		this.removeDeviceBox = function(domNode) {
			$(domNode).fadeOut();
		}

		this._selectedDevice = ko.observable(false);
		this.selectedDevice = ko.computed({
			read:  function()  { return this._selectedDevice(); },
			write: function(val) {
				this._selectedDevice(val);
				window.location.hash = val.id || '';
				$lightbox.toggle(val ? true : false);
			}
		}, this);
		
		/*function addDevice() {
			var selected = devicesViewModel.selectedDevice();
			devicesViewModel.devices.push(new DeviceViewModel(selected));
		}*/
	}

	$(document).ready(function() {
		$.when(api.devices.list(ON_OFF + DIM)
		).done(function(data) {
			if (data.device) {
				$deviceContainer.hide();
				
				var devices = data.device;
				devices.sort(sort_by('name', true, function(a){ return a.toUpperCase() }));
				
				devicesViewModel = new DevicesViewModel(devices);
				ko.applyBindings(devicesViewModel);
						
				var hash = location.hash.slice(1);
				if (hash) {
					$.when(getDevice(hash, true)
					).then(function(device) {
						return devicesViewModel.selectedDevice(device);
					});
				}

				$('#loading').hide()
				$deviceContainer.show();
			} else {
				var error = data.error || 'Unknown error';
				$deviceContainer.text('Error: ' + error);
			}
		});
		
		$lightbox.click(function(e) {
			var $el = $(e.target);
			if ($el.is('#lightbox')) {
				devicesViewModel.selectedDevice(false);
			}
		});
	});

	ko.bindingHandlers.slideButtons = {
		update: function(element, valueAccessor, allBindings) {
			var dimmable = ko.unwrap(valueAccessor());
				
			if (dimmable) {
				var $element = $(element);
				$element.empty();
				$element.append(createSlideButtons());
			}
		}
	};
	
	function getDevice(id, loadAll, onComplete) {
		try {
			id = parseInt(id);
		} catch(e) {
			return;
		}

		var device = ko.utils.arrayFirst(devicesViewModel.devices(), function(item) {
            return item.id == id;
        });

		if (device) {
			if ('model' in device) {
				return device;
			} else {
				var deferred = $.Deferred();
				api.device.info(id, SUPPORTED_METHODS, function(data) {
					device.update(data);
					deferred.resolve(device);
				});
				return deferred;
			}
		}
	}
	
	function createSlideButtons(startValue) {
		var buffer = [];
		for (var val = 0; val < NUM_SLIDES; val++) {
			var textValue = Math.round(100 * val / (NUM_SLIDES - 1));
			var anchor = ACTIONBUTTONTEMPLATE.clone()
				.width(SLIDE_WIDTH + '%')
				.data('val', val)
				.find('a')
					.text(textValue + '%')
					.end()
			buffer.push(anchor);
		}
		return buffer;
	}
</script>
%rebase('layout', title='Devices', name='devices', **locals())