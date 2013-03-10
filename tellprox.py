#!/usr/bin/env python

from bottle import *
from threading import Lock
from tellstick import TellStick
from configobj import ConfigObj
from validate import Validator
from admin_app import admin_ap
import json

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'

TELLSTICK = None
INIT_LOCK = Lock()

# TODO wrap using virtualenv / py2exe
# TODO use CherryPy for Web UI

app = Bottle()

# Setup Tellstick
def initialise_tellstick():
	with INIT_LOCK:
		global TELLSTICK
		TELLSTICK = TellStick()
		TELLSTICK.loadlibrary(config['dll_path'])

@app.route('/test')
def test():
	params = {
		'oauth_version': "1.0",
		'oauth_nonce': oauth.generate_nonce(),
		'oauth_timestamp': int(time.time()),
		'user': 'joestump',
		'photoid': 555555555555
	}
	#token = oauth.Token(key="tok-test-key", secret="tok-test-secret")
	consumer = oauth.Consumer(key="ZUXEVEGA9USTAZEWRETHAQUBUR69U6EF", secret="4e16fe3ecde3f79c2a47a9a8c754556b")
	#params['oauth_token'] = token.key
	params['oauth_consumer_key'] = consumer.key
	url = "http://api.telldus.com"
	req = oauth.Request(method="POST", url=url+'/oauth/requestToken', parameters=params)
	return req

def get_int(key):
	num = request.query.get(key) or ''
	try:
		return int(num)
	except ValueError:
		return num

def get_string(key):
	return request.query.get(key)

@app.route('/<outformat>/devices/list')
def list(outformat='json'):
	supportedMethods = request.query.get('supportedMethods') or 0
	devices = TELLSTICK.devices(supportedMethods)
	devices = [append_client_info(d) for d in devices]
	
	return generate_response({ 'device': devices })

def append_client_info(device):
	global config
	device['client'] = config['client_id']
	device['clientName'] = config['client_name']
	return device

@app.route('/<outformat>/device/add')
def add(outformat):
	global config
	if (config['editable'] is False):
		return { "error" : "Client is not editable" }
	
	# This isn't nice. For the time being assume we have one client with id 1
	clientid = get_int('clientid') or 1
	if (clientid != 1):
		return { "error" : "Client \"" + str(clientid) + "\" not found" }

	resp = TELLSTICK.add(
		get_string('name'),
		get_string('protocol'),
		get_string('model'))
	return generate_response(resp)

@app.route('/<outformat>/device/bell')
def bell(outformat):
	id = request.query.get('id')
	resp = TELLSTICK.bell(id)
	return generate_response(resp)

@app.route('/<outformat>/device/command')
def command(outformat):	
	resp = TELLSTICK.command(
		get_int('id'),
		get_int('method'),
		get_int('value')
	)
	return generate_response(resp)

@app.route('/<outformat>/device/dim')
def dim(outformat):
	resp = TELLSTICK.dim(
		get_int('id'),
		get_int('level'))
	return generate_response(resp)

@app.route('/<outformat>/device/down')
def down(outformat):
	resp = TELLSTICK.down(get_int('id'))
	return generate_response(resp)

@app.route('/<outformat>/device/info')
def info(outformat):
	device = TELLSTICK.read_device(
		get_int('id'),
		get_int('supportedMethods') or 0,
		True)
	device = append_client_info(device)
	return generate_response(device)
	
@app.route('/<outformat>/device/learn')
def learn(outformat):
	resp = TELLSTICK.learn(get_int('id'))
	return generate_response(resp)

@app.route('/<outformat>/device/remove')
def remove(outformat):
	resp = TELLSTICK.remove(get_int('id'))
	return generate_response(resp)

@app.route('/<outformat>/device/setName')
def setName(outformat):
	resp = TELLSTICK.set_name(get_int('id'), get_string('name'))
	return generate_response(resp)

@app.route('/<outformat>/device/setModel')
def setModel(outformat):
	resp = TELLSTICK.set_model(get_int('id'), get_string('model'))
	return generate_response(resp)

@app.route('/<outformat>/device/setProtocol')
def setProtocol(outformat):
	resp = TELLSTICK.set_protocol(get_int('id'), get_string('protocol'))
	return generate_response(resp)

@app.route('/<outformat>/device/setParameter')
def setParameter(outformat):
	resp = TELLSTICK.set_parameter(
		get_int('id'),
		get_string('parameter'),
		get_string('value'))
	return generate_response(resp)

@app.route('/<outformat>/device/stop')
def stop(outformat):
	resp = TELLSTICK.stop(get_int('id'))
	return generate_response(resp)

@app.route('/<outformat>/device/turnOn')
def turnOn(outformat):
	resp = TELLSTICK.on(get_int('id'))
	return generate_response(resp)

@app.route('/<outformat>/device/turnOff')
def turnOff(outformat):
	resp = TELLSTICK.off(get_int('id'))
	return generate_response(resp)

@app.route('/<outformat>/device/up')
def up(outformat):
	resp = TELLSTICK.up(get_int('id'))
	return generate_response(resp)

def generate_response(input):
	# Shift the path to get the first 'folder'
	request.path_shift(1)
	if (request.script_name.lower() == '/xml/'):
		return "Not implemented yet"

	converted = json.dumps(input)
	callback_function = request.query.get('callback')
	if callback_function:
		converted = callback_function + '(' + converted + ');'
	
	response.content_type = 'application/json'
	return converted

@app.route('/all')
def index():
	devices = { 'device': TELLSTICK.devices() }
	json_response = json.dumps(devices)
	return generate_response(json_response)

@app.route('/<id>/<level>')
def index(id, level):
	if level.lower() == 'on':
		TELLSTICK.on(id)
	elif level.lower() == 'off':
		TELLSTICK.off(id)
	else:
		level = int(level)
		TELLSTICK.dim(id, level)
		
	json_response = "{result:true}"
	callback_function = request.query.get('callback')
	if callback_function:
		json_response = ''.join([callback_function, '(', json_response, ');'])
	
	response.content_type = 'application/json'
	return json_response

config = ConfigObj(CONFIG_PATH, configspec=CONFIG_SPEC)
validator = Validator()
result = config.validate(validator, copy=True)

if result is False:
	print "Config file validation failed"
	sys.exit(1)

# Write out default values
config.write()

initialise_tellstick()
debug(config['debug'])
run(app, host=config['host'], port=config['port'], reloader=config['debug'])