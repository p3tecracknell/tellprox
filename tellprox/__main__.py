#!/usr/bin/env python

import sys
if sys.version_info < (2, 5):
    print "Sorry, requires Python 2.5, 2.6 or 2.7."
    sys.exit(1)

import tellstick_api
import json
import bottle

from configobj import ConfigObj
from validate import Validator

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'

config = None
app = bottle.Bottle()

# TODO wrap using virtualenv / py2exe
def main():
	config = ConfigObj(CONFIG_PATH, configspec = CONFIG_SPEC)
	validator = Validator()
	result = config.validate(validator, copy = True)

	if result is False:
		print "Config file validation failed"
		sys.exit(1)

	# Write out default values
	config.write()
	
	tellstick_api.TellstickAPI(app, config)
	
	bottle.debug(config['debug'])
	bottle.run(app,
		host = config['host'],
		port = config['port'],
		reloader = config['debug'])

@app.route('/')
def home_page():
	return bottle.static_file('index.html', root='./static')

@app.route('/config')
def home_page():
	return bottle.static_file('config.html', root='./static')

@app.route('/ui')
def home_page():
	return bottle.static_file('ui.html', root='./static')
	
@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return bottle.static_file(filepath, root='./static')

@app.route('/api/config', method='ANY')
def get_config():
	rows = [ {'name': key, 'value': value, 'editor': 'text'}
		for key, value in config.iteritems() ]
	return json.dumps({"total":len(config),"rows": rows })

if __name__ == "__main__":
	main()