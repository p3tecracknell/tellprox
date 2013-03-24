#!/usr/bin/env python

from bottle import *
from threading import Lock
from tellstick import TellStick
import json

TELLSTICK = None
config = None
INIT_LOCK = Lock()

app = Bottle()

def set_config(in_config):
	global config
	config = in_config

	# Setup Tellstick
	with INIT_LOCK:
		global TELLSTICK
		TELLSTICK = TellStick()
		TELLSTICK.loadlibrary(config['library_name'])

@app.route('/<out_format:re:(?i)(xml|json)>/<ftype:path>/<func:path>', method=['GET', 'POST'])
def route_all(out_format, ftype, func):
	ftype = ftype.strip().lower()
	func = func.strip().lower()
	
	if (ftype == 'devices' and func == 'list'):
		# Only one function within devices, return it here
		resp = { 'device': [
			append_client_info(d) for d in
			TELLSTICK.devices(get_int('supportedMethods'))
			] }
	
	elif (ftype == 'device'):
		resp = device_func(func)
	
	elif (ftype == 'group'):
		resp = 'not implemented yet'
		
	elif (ftype == 'scheduler'):
		resp = 'not implemented yet'

	elif (ftype == 'sensors'):
		resp = 'not implemented yet'
	
	elif (ftype == 'sensor'):
		resp = 'not implemented yet'
	
	else:
		return "404" #todo
	
	return format_response(resp, out_format)

def device_func(func):
	global config
	if (func == 'add'):
		if (config['editable'] is False):
			return { "error" : "Client is not editable" }

		clientid = get_int('clientid') or 1
		if (clientid != config['client_id']):
			return { "error" : "Client \"" + str(clientid) + "\" not found" }

		return TELLSTICK.add_device(
			get_string('name'),
			get_string('protocol'),
			get_string('model'))
	
	elif (func == 'bell'):
		return TELLSTICK.bell(get_int('id'))
	
	elif (func == 'command'):
		return TELLSTICK.command(
			get_int('id'),
			get_int('method'),
			get_int('value')
		)

	elif (func == 'dim'):
		return TELLSTICK.dim(
			get_int('id'),
			get_int('level'))
		
	elif (func == 'down'):
		return TELLSTICK.down(get_int('id'))

	elif (func == 'info'):
		return append_client_info(
			TELLSTICK.read_device(
				get_int('id'),
				get_int('supportedMethods') or 0,
				True))
	
	elif (func == 'learn'):
		return TELLSTICK.learn(get_int('id'))
		
	elif (func == 'remove'):
		return TELLSTICK.remove_device(get_int('id'))

	elif (func == 'setname'):
		return TELLSTICK.set_name(get_int('id'), get_string('name'))

	elif (func == 'setmodel'):
		return TELLSTICK.set_model(get_int('id'), get_string('model'))
	
	elif (func == 'setprotocol'):
		return TELLSTICK.set_protocol(get_int('id'), get_string('protocol'))
	
	elif (func == 'setparameter'):
		return TELLSTICK.set_parameter(
		get_int('id'),
		get_string('parameter'),
		get_string('value'))
	
	elif (func == 'stop'):
		return TELLSTICK.stop(get_int('id'))

	elif (func == 'turnon'):
		return TELLSTICK.on(get_int('id'))

	elif (func == 'turnoff'):
		return TELLSTICK.off(get_int('id'))

	elif (func == 'up'):
		return TELLSTICK.up(get_int('id'))
		
	else:
		return "function not recognised"

def format_response(input, out_format):
	if (out_format.lower() == 'xml'):
		#converted = xmlrpclib.dumps(({'vol':'III', 'title':'Magical Unicorn'},))
		converted = "not implemented"
		response.content_type = 'application/xml'
	else:
		converted = json.dumps(input, indent = 4 if config['pretty_print'] else None)
		callback_function = request.query.get('callback')
		if callback_function:
			converted = callback_function + '(' + converted + ');'
		
		response.content_type = 'application/json'
	return converted

# Add client id and name to a device using config
# defined by the user
def append_client_info(device):
	global config
	device['client'] = config['client_id']
	device['clientName'] = config['client_name']
	return device

# Helper Functions
def get_int(key):
	num = request.query.get(key) or ''
	try:
		return int(num)
	except ValueError:
		return num

def get_string(key):
	return request.query.get(key)
	return device