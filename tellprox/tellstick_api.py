from bottle import *
from telldus.constants import *
import bottle_helpers as bh
import telldus.telldus as td

class MSensor(object):
    def __init__(self, protocol, model, id, datatypes):
        super(MSensor, self).__init__()
        self.protocol = protocol
        self.model = model
        self.id = id
        self.datatypes = datatypes
        #self.lib = Library()

    def value(self, datatype):
        return MSensorValue('val', 'timestamp')

    def has_temperature(self):
        return self.datatypes & TELLSTICK_TEMPERATURE != 0

    def has_humidity(self):
        return self.datatypes & TELLSTICK_HUMIDITY != 0

    def temperature(self):
        return self.value(TELLSTICK_TEMPERATURE)

    def humidity(self):
        return self.value(TELLSTICK_HUMIDITY)

class MSensorValue(object):
    __slots__ = ["value", "timestamp"]

    def __init__(self, value, timestamp):
        super(MSensorValue, self).__init__()
        self.value = value
        self.timestamp = timestamp

class TellstickAPI(object):
	""" Mimick Telldus Live """
	config = None
	core = td.TelldusCore()

	def __init__(self, app, config):
		self.config = config
		self.app = app
		app.route('/<out_format:re:(?i)(xml|json)>/<ftype:path>/<func:path>',
			method = ['GET', 'POST'],
			callback = self.route_all)
		self.load_devices()
		self.load_sensors()
	
	def load_devices(self):
		""" Read in all devices using telldus-py library and convert into
			id keyed dictionary """
		self.devices = { device.id: device for device in self.core.devices() }
	
	def load_sensors(self):
		""" Read in all sensors using telldus-py library and convert into
			id keyed dictionary """
		self.sensors = { sensor.id: sensor for sensor in self.core.sensors()}
		self.sensors['9998'] = MSensor('prot', 'model', 9998, TELLSTICK_TEMPERATURE + TELLSTICK_HUMIDITY)
		self.sensors['9999'] = MSensor('prot', 'model', 9999, TELLSTICK_TEMPERATURE + TELLSTICK_HUMIDITY)

	def route_all(self, out_format, ftype, func):
		""" Root level routing for all tellstick functionality """
		ftype = ftype.strip().lower()
		func = func.strip().lower()
		
		if   (ftype == 'devices' and func == 'list'): resp = self.route_devices()
		elif (ftype == 'device'):                     resp = self.route_device(func)
		elif (ftype == 'clients' and func == 'list'): resp = self.route_clients()
		elif (ftype == 'client'):                     resp = self.route_client()
		elif (ftype == 'group'):                      resp = 'not implemented yet'
		elif (ftype == 'scheduler'):                  resp = 'not implemented yet'
		elif (ftype == 'sensors' and func == 'list'): resp = self.route_sensors()
		elif (ftype == 'sensor'):                     resp = self.route_sensor(func)
		else:                                         bh.raise404()
		
		return bh.format_response(resp, out_format, self.config['pretty_print'])

	def route_devices(self):
		supportedMethods = self.get_supported_methods()
		return { 'device': [
			self.map_device_to_json(device, supportedMethods)
				for k, device in self.devices.iteritems()
		]}

	def route_device(self, func):
		if (func == 'add'): resp = self.add_device()
		else:
			""" With the only function that does not require ID out of the way, 
				determine the device we want to interact with """
			id = bh.get_int('id')			
			if (self.devices.has_key(id)):
				device = self.devices[id]
				if (func == 'info'):
					return self.map_device_to_json(device, self.get_supported_methods())
				elif (func[:3] == 'set'): resp = self.device_set_parameter(device, func[3:])
				elif (func == 'command'):
					resp = self.device_command(device, bh.get_int('method'), bh.get_int('value'))
				else: resp = self.device_command(device, func, bh.get_int('level'))
				if resp is None: bh.raise404()
			else:
				resp = "Device " + "\"" + str(id) + "\" not found!"
		
		return self.map_response(resp)

	def add_device(self):
		if (self.config['editable'] is False):
			return "Client is not editable"

		clientid = self.get_client_id()
		if (clientid != self.config['client_id']):
			return "Client \"" + str(clientid) + "\" not found!"

		# TODO try/catch handling
		self.core.add_device(
			bh.get_string('name'),
			bh.get_string('protocol'),
			bh.get_string('model'))
		
		return TELLSTICK_SUCCESS

	def device_command(self, device, func, value = ''):
		# TODO replace with try/catch
		if   (func == 'bell'):    device.bell()
		elif (func == 'dim'):     device.dim(value)
		elif (func == 'down'):    device.down()
		elif (func == 'learn'):   device.learn()
		elif (func == 'remove'):  device.remove()
		elif (func == 'stop'):    device.stop()
		elif (func == 'turnon'):  device.turn_on()
		elif (func == 'turnoff'): device.turn_off()
		elif (func == 'up'):      device.up()
		
		return TELLSTICK_SUCCESS
	
	def device_set_parameter(self, device, attr):
		if (attr == 'parameter'):
			resp = device.set_parameter(bh.get_string('parameter'), bh.get_string('value'))
		elif attr in ['name', 'model', 'protocol']:
			value = bh.get_string(attr)
			if value is None: return "Attribute \"" + attr + "\" not found"
			resp = device.__setattr__(attr, value)
		else: bh.raise404()
		if resp: return TELLSTICK_SUCCESS
		else: return TELLSTICK_ERROR_NOT_FOUND
				
	def route_clients(self):
		return { 'client': [self.get_client_info()] }

	def route_client(self):
		clientid = self.get_client_id()
		if (clientid != config['client_id']):
			return { "error" : "Client \"" + str(clientid) + "\" not found!" }
		return self.get_client_info()

	def route_sensors(self):
		includeIgnored = True if bh.get_int('includeIgnored') == 1 else 0
		return { 'sensor': [
			self.map_sensor_to_json(sensor)
				for k, sensor in self.sensors.iteritems()
				if includeIgnored or self.is_ignored_sensor(sensor.id)
		]}
		
	def is_ignored_sensor(self, id):
		return str(id) in self.config['ignored_sensors']
	
	def route_sensor(self, func):
		# The ID should be an integer, but we store them in the dictionary as
		# strings, so treat as such
		id = str(bh.get_int('id'))
		resp = TELLSTICK_SUCCESS
		if (self.sensors.has_key(id)):
			sensor = self.sensors[id]
			if (func == 'info'):
				return self.map_sensor_to_json(sensor, True)
			elif (func == 'setignore'):
				if (bh.get_int('ignore') == 1):
					self.config['ignored_sensors'].append(id)
				else:
					self.config['ignored_sensors'].remove(id)
				self.save_sensor_ignore_list()
			elif (func == 'setname'):
				return "not implemented"
				
			if resp is None: bh.raise404()
		else:
			resp = "Sensor " + "\"" + str(id) + "\" not found!"
		
		return self.map_response(resp)
	
	def save_sensor_ignore_list(self):
		self.config['ignored_sensors'] = list(set(self.config['ignored_sensors']))
		self.config.write()
	
	# Add client id and name to a device using config
	# defined by the user
	def append_client_info(self, device):
		extra = {
			'client': self.config['client_id'] or 1,
			'clientName': self.config['client_name'] or '',
			'editable': 1 if self.config['editable'] else 0
		}
		return dict(device.items() + extra.items())

	def device_type_to_string(self, type):
		if (type == TELLSTICK_TYPE_DEVICE):
			return 'device'
		elif (type == TELLSTICK_TYPE_GROUP):
			return 'group'
		else:
			return 'scene'

	def map_device_to_json(self, device, methods_supported):
		json = {
			'id': device.id,
			'name': device.name,
			'state': device.last_sent_command(methods_supported),
			'statevalue': device.last_sent_value(),
			'methods': device.methods(methods_supported),
			'type': self.device_type_to_string(device.type),
			'online': 1,
		}
		return self.append_client_info(json)
	
	def map_sensor_to_json(self, sensor, extra=False):
		lastUpdated = -1		
		sensor_data = []
		for type in [
			{'name': 'temp',     'key': TELLSTICK_TEMPERATURE },
			{'name': 'humidity', 'key': TELLSTICK_HUMIDITY }
		]:
			if sensor.datatypes & type['key'] != 0:
				svalue = sensor.value(type['key'])
				lastUpdated = svalue.timestamp
				sensor_data.append({'name': type['name'], 'value': svalue.value})
		
		json = {
			'id': sensor.id,
			'name': "TODO",
			'lastUpdated': lastUpdated,
			'ignored': 1 if self.is_ignored_sensor(sensor.id) else 0,
			'online': 1
		}
		
		if extra:
			extra_json = {
				'data': sensor_data,
				'protocol': sensor.protocol,
				'sensorId': 'TODO',
				'timezoneoffset': 'TODO'
			}
			json = dict(json.items() + extra_json.items())
		
		return self.append_client_info(json)

	def get_client_info(self):
		return {
			'id': config['client_id'] or 1,
			'uuid':'00000000-0000-0000-0000-000000000000',
			'name':config['client_name'] or '',
			'online': '1',
			'editable': 1 if config['editable'] else 0,
			'version':'0.2',
			'type':'TellProx'
		}

	def map_response(self, cmdresp, id = '', method = ''):
		if (cmdresp == TELLSTICK_SUCCESS):
			return { "status" : "success" }
		elif isinstance(cmdresp, int):
			id = str(id)
			if (cmdresp == TELLSTICK_ERROR_DEVICE_NOT_FOUND):
				msg = "Device " + "\"" + id + "\" not found!"
			elif (cmdresp == TELLSTICK_ERROR_BROKEN_PIPE):
				msg = "Broken pipe"
			elif (cmdresp == TELLSTICK_ERROR_COMMUNICATING_SERVICE):
				msg = "Communicating service"
			elif (cmdresp == TELLSTICK_ERROR_COMMUNICATION):
				msg = "Communication"
			elif (cmdresp == TELLSTICK_ERROR_CONNECTING_SERVICE):
				msg = "Cannot connect to service"
			elif (cmdresp == TELLSTICK_ERROR_METHOD_NOT_SUPPORTED):
				msg = "Device \"" + id + "\" does not support method \"" + str(method) + "\""
			elif (cmdresp == TELLSTICK_ERROR_NOT_FOUND):
				msg = "Not found"
			elif (cmdresp == TELLSTICK_ERROR_PERMISSION_DENIED):
				msg = "Permission denied"
			elif (cmdresp == TELLSTICK_ERROR_SYNTAX):
				msg = "Syntax error"
			else: msg = "Unknown response"
		else: msg = str(cmdresp)
		return { "error" : msg }

	""" Helper Functions """
	def get_supported_methods(self):
		return bh.get_int('supportedMethods') or 0

	def get_client_id(self):
		return bh.get_int('clientid') or 1