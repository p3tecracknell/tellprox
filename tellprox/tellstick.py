from bottle import *
from telldus.constants import *
from msensor import *
from tasensor import *
import bottle_helpers as bh
import telldus.telldus as td
	
class TellstickAPI(object):
	""" Mimick Telldus Live """
	config = None
	core = td.TelldusCore()
	sensors = {}

	def __init__(self, api, config):
		self.config = config
		
		self.load_devices()
		self.load_sensors()
		
		api.add_route('devices', self.route_devices)
		api.add_route('device', self.route_device)
		api.add_route('clients', self.route_clients)
		api.add_route('client', self.route_client)
		api.add_route('sensors', self.route_sensors)
		api.add_route('sensor', self.route_sensor)
		#api.add_route('group', 'not implemented yet'
		#api.add_route('scheduler', 'not implemented yet'

	
	def load_devices(self):
		""" Read in all devices using telldus-py library and convert into
			id keyed dictionary """
		self.devices = { device.id: device for device in self.core.devices() }
	
	def load_sensors(self):
		""" Read in all sensors using telldus-py library and convert into
			id keyed dictionary """
		
		sensors = self.core.sensors()
		if (self.config['debug']):
			sensors.append(MSensor('prot1', 'model1', 9998, TELLSTICK_TEMPERATURE))
			sensors.append(MSensor('prot2', 'model2', 9999, TELLSTICK_TEMPERATURE + TELLSTICK_HUMIDITY))
		
		self.sensors = {
			str(rawsensor.id) : TASensor(self.config, rawsensor)
				for rawsensor in sensors
		}

	def route_devices(self, func):
		if not func == 'list': bh.raise404()
		
		supportedMethods = self.get_supported_methods()
		self.load_devices()
		return { 'device': [
			self.device_to_dict(device, supportedMethods, False)
				for k, device in self.devices.iteritems()
		]}

	def route_device(self, func):
		if (func == 'add'):
			id = ''
			resp = self.add_device()
			if type(resp) is td.Device:
				id = resp.id
				resp = TELLSTICK_SUCCESS
			return self.map_response(resp, id)
		else:
			""" With the only function that does not require ID out of the way, 
				determine the device we want to interact with """
			id = bh.get_int('id')
			self.load_devices()
			if (self.devices.has_key(id)):
				device = self.devices[id]
				if (func == 'info'):
					return self.device_to_dict(device, self.get_supported_methods(), True)
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

		clientid = bh.get_int('id')
		if (clientid != self.config['client_id']):
			return "Client \"" + str(clientid) + "\" not found!"

		try:
			return self.core.add_device(
				bh.get_string('name'),
				bh.get_string('protocol'),
				bh.get_string('model'))
		except Exception as e:
			return e

	def device_command(self, device, func, value = ''):
		try:
			if   (func == 'bell'):    device.bell()
			elif (func == 'dim'):     device.dim(value)
			elif (func == 'down'):    device.down()
			elif (func == 'learn'):   device.learn()
			elif (func == 'remove'):  device.remove()
			elif (func == 'stop'):    device.stop()
			elif (func == 'turnon'):  device.turn_on()
			elif (func == 'turnoff'): device.turn_off()
			elif (func == 'up'):      device.up()
			elif (func == 'toggle'): self.toggle_device(device)
		except Exception as e:
			return e
		return TELLSTICK_SUCCESS
	
	def toggle_device(self, device):
		if device.last_sent_command(TELLSTICK_TURNON + TELLSTICK_TURNOFF) == 1:
			device.turn_off()
		else:
			device.turn_on()
	
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
				
	def route_clients(self, func):
		if not func == 'list': bh.raise404()
		return { 'client': [self.get_client_info()] }

	def route_client(self, func):
		if not func == 'info': bh.raise404()
		clientid = clientid = bh.get_int('id')
		
		if (clientid != self.config['client_id']):
			return { "error" : "Client \"" + str(clientid) + "\" not found!" }
		return self.get_client_info()

	def route_sensors(self, func):
		if not func == 'list': bh.raise404()
		
		self.load_sensors()
		includeIgnored = True if bh.get_int('includeignored') == 1 else False
		return { 'sensor': [
			self.sensor_to_dict(sensor, False)
				for id, sensor in self.sensors.iteritems()
				if includeIgnored or int(sensor.ignore) == 0
		]}
	
	def route_sensor(self, func):
		# The ID should be an integer, but we store them in the dictionary as
		# strings, so treat as such
		id = str(bh.get_int('id'))
		
		self.load_sensors()
		resp = TELLSTICK_SUCCESS
		if (self.sensors.has_key(id)):
			sensor = self.sensors[id]
			if (func == 'info'):
				return self.sensor_to_dict(sensor, True)
			elif (func == 'setignore'):
				sensor.ignore = 1 if bh.get_int('ignore') == 1 else 0
			elif (func == 'setname'):
				sensor.name = bh.get_string('name')
				
			if resp is None: bh.raise404()
		else:
			resp = "Sensor " + "\"" + str(id) + "\" not found!"
		
		return self.map_response(resp)
	
	def editable(self):
		return 1 if self.config['editable'] else 0
	
	def client(self):
		return self.config['client_id'] or 1
	
	def clientName(self):
		return self.config['client_name'] or ''

	def device_type_to_string(self, type):
		if (type == TELLSTICK_TYPE_DEVICE):
			return 'device'
		elif (type == TELLSTICK_TYPE_GROUP):
			return 'group'
		else:
			return 'scene'

	""" Converts a device into a dictionary ready for outputting to json/xml
		info is used to indicate whether it is used to output for info as per spec
	"""
	def device_to_dict(self, device, methods_supported, info):
		json = {
			'id':         device.id,
			'name':       device.name,
			'state':      device.last_sent_command(methods_supported),
			'statevalue': device.last_sent_value(),
			'methods':    device.methods(methods_supported),
			'type':       self.device_type_to_string(device.type),
			'online':     1,
			'editable':   self.editable()
		}
		
		if info:
			json['protocol'] = None # TODO
			json['model']    = None  # TODO
		else:
			json['client'] = self.client()
			json['clientName'] = self.clientName()
			json = bh.set_attribute(json)
			
		return json
	
	def sensor_to_dict(self, sensor, info):
		# Set default value in case we get back nothing
		lastUpdated = -1
		
		# Populate sensor data using calls to core library
		sensor_data = []
		for type in [
			{'name': 'temp',     'key': TELLSTICK_TEMPERATURE },
			{'name': 'humidity', 'key': TELLSTICK_HUMIDITY }
		]:
			if sensor.raw.datatypes & type['key'] != 0:
				svalue = sensor.raw.value(type['key'])
				lastUpdated = svalue.timestamp
				sensor_data.append({'name': type['name'], 'value': svalue.value})
		
		json = {
			'id'         : sensor.raw.id,
			'name'       : sensor.name,
			'lastUpdated': lastUpdated,
			'ignored'    : int(sensor.ignore),
			'online'     : 1,
			'editable'   : self.editable(),
			'client'     : self.client()
		}
		
		if info:
			extra_json = {
				'data': sensor_data,
				'protocol': sensor.raw.protocol,
				'sensorId': sensor.raw.id,
				'timezoneoffset': 7200
			}
			json = dict(json.items() + extra_json.items())
		else:
			json['clientName'] = self.clientName()
		return json

	def get_client_info(self):
		return {
			'id': self.config['client_id'] or 1,
			'uuid':'00000000-0000-0000-0000-000000000000',
			'name':self.config['client_name'] or '',
			'online': '1',
			'editable': 1 if self.config['editable'] else 0,
			'version':'0.21',
			'type':'TellProx'
		}

	def map_response(self, cmdresp, id = '', method = ''):
		if (cmdresp == TELLSTICK_SUCCESS):
			resp = { "status" : "success" }
			if not id == '':
				resp['id'] = id
			return resp
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