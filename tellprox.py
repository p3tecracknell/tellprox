#!/usr/bin/env python

from bottle import *
from configobj import ConfigObj
from validate import Validator
import tellstick_api
import json

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'

# TODO wrap using virtualenv / py2exe
app = Bottle()

config = ConfigObj(CONFIG_PATH, configspec=CONFIG_SPEC)
validator = Validator()
result = config.validate(validator, copy=True)

if result is False:
	print "Config file validation failed"
	sys.exit(1)

# Write out default values
config.write()

tellstick_api.set_config(config)
app.mount('/json', tellstick_api.app)

@app.route('/')
def server_static():
	return static_file('index.html', root='.')

@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return static_file(filepath, root='./static')

debug(config['debug'])
run(app,
	host = config['host'],
	port = config['port'],
	reloader = config['debug'])