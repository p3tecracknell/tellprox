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
	initialise_tellstick()

# Setup Tellstick
def initialise_tellstick():
	with INIT_LOCK:
		global TELLSTICK
		TELLSTICK = TellStick()
		TELLSTICK.loadlibrary(config['dll_path'])

def get_int(key):
	num = request.query.get(key) or ''
	try:
		return int(num)
	except ValueError:
		return num

def get_string(key):
	return request.query.get(key)

@app.route('/devices/list')
def list():
	devices = TELLSTICK.devices(get_int('supportedMethods'))
	devices = [append_client_info(d) for d in devices]
	
	return generate_response({ 'device': devices })

def append_client_info(device):
	global config
	device['client'] = config['client_id']
	device['clientName'] = config['client_name']
	return device

@app.route('/device/add')
def add():
	global config
	if (config['editable'] is False):
		return { "error" : "Client is not editable" }
	
	# This isn't nice. For the time being assume we have one client with id 1
	clientid = get_int('clientid') or 1
	if (clientid != config['client_id']):
		return { "error" : "Client \"" + str(clientid) + "\" not found" }

	resp = TELLSTICK.add(
		get_string('name'),
		get_string('protocol'),
		get_string('model'))
	return generate_response(resp)

@app.route('/device/bell')
def bell():
	resp = TELLSTICK.bell(get_int('id'))
	return generate_response(resp)

@app.route('/device/command')
def command():	
	resp = TELLSTICK.command(
		get_int('id'),
		get_int('method'),
		get_int('value')
	)
	return generate_response(resp)

@app.route('/device/dim')
def dim():
	resp = TELLSTICK.dim(
		get_int('id'),
		get_int('level'))
	return generate_response(resp)

@app.route('/device/down')
def down():
	resp = TELLSTICK.down(get_int('id'))
	return generate_response(resp)

@app.route('/device/info')
def info():
	device = TELLSTICK.read_device(
		get_int('id'),
		get_int('supportedMethods') or 0,
		True)
	device = append_client_info(device)
	return generate_response(device)
	
@app.route('/device/learn')
def learn():
	resp = TELLSTICK.learn(get_int('id'))
	return generate_response(resp)

@app.route('/device/remove')
def remove():
	resp = TELLSTICK.remove(get_int('id'))
	return generate_response(resp)

@app.route('/device/setName')
def setName():
	resp = TELLSTICK.set_name(get_int('id'), get_string('name'))
	return generate_response(resp)

@app.route('/device/setModel')
def setModel():
	resp = TELLSTICK.set_model(get_int('id'), get_string('model'))
	return generate_response(resp)

@app.route('/device/setProtocol')
def setProtocol():
	resp = TELLSTICK.set_protocol(get_int('id'), get_string('protocol'))
	return generate_response(resp)

@app.route('/device/setParameter')
def setParameter():
	resp = TELLSTICK.set_parameter(
		get_int('id'),
		get_string('parameter'),
		get_string('value'))
	return generate_response(resp)

@app.route('/device/stop')
def stop():
	resp = TELLSTICK.stop(get_int('id'))
	return generate_response(resp)

@app.route('/device/turnOn')
def turnOn():
	resp = TELLSTICK.on(get_int('id'))
	return generate_response(resp)

@app.route('/device/turnOff')
def turnOff():
	resp = TELLSTICK.off(get_int('id'))
	return generate_response(resp)

@app.route('/device/up')
def up():
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