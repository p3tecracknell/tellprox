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
bottle.TEMPLATE_PATH.insert(0, './tellprox/views')
root_app = bottle.Bottle()
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
	ConfigAPI(api, config, validator)
	
	if config['webroot']:
		root_app.mount(config['webroot'], app)
	else:
		root_app.merge(app)
	
	bottle.run(root_app,
		host = config['host'],
		port = config['port'],
		debug = config['debug'],
		reloader = config['debug'],
		server = 'cherrypy')

	# Write out default values
	config.write()

def render_template(view):
	vars = {
		'apikey' : config['apikey'] or ''
	}
	return template(view, vars);

@app.route('/')
def home_page():
	return "<html><body><script>window.location.replace(window.location.href.replace(/\/?$/, '/') + 'devices')</script></body></html>"
	
@app.route('/devices')
def devices():
	return render_template('devices')

@app.route('/api')
def devices():
	return render_template('api')

@app.route('/config')
def home_page():
	return render_template('config')

@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return bottle.static_file(filepath, root='./tellprox/static')

if __name__ == "__main__":
	main()