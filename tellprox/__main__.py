#!/usr/bin/env python

import sys
if sys.version_info < (2, 5):
    print "Sorry, requires Python 2.5, 2.6 or 2.7."
    sys.exit(1)

import json, bottle

from api import API
from tellstick import TellstickAPI
from config import ConfigAPI
from bottle import template, redirect
from configobj import ConfigObj
from validate import Validator

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'
  
config = None
app = bottle.Bottle()

def main():
	global config
	config = ConfigObj(CONFIG_PATH, configspec = CONFIG_SPEC)
	validator = Validator()
	result = config.validate(validator, copy = True)

	if result is False:
		print "Config file validation failed"
		sys.exit(1)
	
	api = API(app, config)
	TellstickAPI(api, config)
	ConfigAPI(api, config)
	
	bottle.run(app,
		host = config['host'],
		port = config['port'],
		debug = config['debug'],
		reloader = config['debug'],
		server = 'cherrypy')
	
	# Write out default values
	config.write()
	
@app.route('/')
def home_page():
	webroot = config['webroot'] + '/' or ''
	redirect(webroot + 'devices')
	
@app.route('/devices')
def devices():
	return template('devices')

@app.route('/api')
def devices():
	return template('api')

@app.route('/config')
def home_page():
	return template('config')

@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return bottle.static_file(filepath, root='./static')

#@app.route('/api/config', method='ANY')
#def get_config():
#	rows = [ {'name': key, 'value': value, 'editor': 'text'}
#		for key, value in config.iteritems() ]
#	return json.dumps({"total":len(config),"rows": rows })

if __name__ == "__main__":
	main()