define(['plugins/http', 'durandal/app', 'knockout', 'services/helpers', 'services/api'], function (http, app, ko, helpers, api2) {
	// Constants
	var OFF = 0,
		ON	= 1,
		DIM = 16,
		ON_OFF = OFF + ON,
		SUPPORTED_METHODS = ON_OFF + DIM;
	
	numSlideButtons = 6;
	
	function DeviceViewModel(device) {
		var me = this;
		
		this.id = device.id;
		this.name = ko.observable(device.name);
		this.methods = ko.observable(device.methods);
		this._state = ko.observable(device.state == 2 ? OFF : ON);
		this._statevalue = ko.observable(device.statevalue);
		
		this.state = ko.computed({
			read:  function()  { return this._state(); },
			write: function(val) {
				this._state(val);
				if (val == ON) api2.device.turnon(this.id);
				else api2.device.turnoff(this.id);
			}
		}, this);
		
		this.statevalue = ko.computed({
			read:  function()  {
				return Math.round(this._statevalue() / 255 * (numSlideButtons - 1));
			},
			write: function(val) {
				val = Math.round(255 * val / (numSlideButtons - 1));
				this._statevalue(val);
				if (val === 0) api2.device.turnoff(this.id);
				else api2.device.dim(this.id, val);
			}
		}, this);			
		
		this.setOn = function() { this.state(ON); };
		this.setOff = function() { this.state(OFF); };
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
		
		this.removeDevice = function() {
			//access parent and remove
			console.log('remove device');
			// TODO: hide modal
		}
			
		// TODO use mapping plugin
		this.update = function(device) {
			this.name(device.name);
			this.methods(device.methods);
			if ('model' in device) {
				this.model = device.model;
			}
		};
	}
	
	ko.bindingHandlers.applySelect = {
		update: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
			var $el = $(element);
			$el.find('.dropdown-toggle').dropdown();
		}
	},
	
	function getDevice(id, loadAll, onComplete) {
		try {
			id = parseInt(id, 10);
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
				api2.device.info(id, SUPPORTED_METHODS, function(data) {
					device.update(data);
					deferred.resolve(device);
				});
				return deferred;
			}
		}
	}
	
	var devices = {
		displayName: 'Devices',
		devices: ko.observableArray([]),
		errorMessage: ko.observable(''),
		removeDeviceBox: function(domNode) {
			$(domNode).fadeOut();
		},

		activate: function () {
			//the router's activator calls this function and waits for it to complete before proceding
			if (this.devices().length > 0) {
				return;
			}
			
			var me = this;

			return $.when(api2.devices.list(ON_OFF + DIM)
			).done(function(data) {
				if (data.device) {
					data.device.sort(helpers.sort_by('name', true, function(a){
						return a.toUpperCase();
					}));
		
					var devices = $.map(data.device, function(device) {
						return new DeviceViewModel(device);
					});
					me.devices(devices);

				} else {
					var error = data.error || 'Unknown error';
					me.errorMessage('Error: ' + error);
				}
			});
		},
		onDeviceRender: function(item) {
		},
		removeDevice: function(item) {
			this.devices.remove(this);
			api2.device.remove(this.id);
		},
		selectDevice: function(item) {
			//the app model allows easy display of modal dialogs by passing a view model
			//views are usually located by convention, but you an specify it as well with viewUrl
			item.viewUrl = 'views/device';
			app.showDialog(item);
		}
	};
	
	return devices;
});