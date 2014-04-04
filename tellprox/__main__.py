#!/usr/bin/env python

import sys
if sys.version_info < (2, 5):
    print "Sorry, requires Python 2.5, 2.6 or 2.7."
    sys.exit(1)

import json, bottle
import sys, os
import utilities
import urllib

# Child APIs
from api import API
from tellstick import TellstickAPI
from config import ConfigAPI
from scheduler import Scheduler
from schedulerApi import SchedulerAPI

# Resources
from bottle import template, request
from configobj import ConfigObj
from validate import Validator
from beaker.middleware import SessionMiddleware
from werkzeug.security import check_password_hash

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'

config = ConfigObj(CONFIG_PATH, configspec = CONFIG_SPEC)
bottle.TEMPLATE_PATH.insert(0, utilities.full_path('/views'))
root_app = bottle.Bottle()
app = bottle.Bottle()
api = None

def main():
	global api
	validator = Validator()
	result = config.validate(validator, copy = True)

	if result is False:
		print "Config file validation failed"
		sys.exit(1)

	api = API(app, config)
	tellstick = TellstickAPI(api, config)
	ConfigAPI(api, config, validator)
	
	# TODO enable/disable scheduler here?
	scheduler = Scheduler(config, tellstick)
	SchedulerAPI(api, config, scheduler)
	
	if not config['installed']:
		api.install()
	
	if config['webroot']:
		root_app.mount(config['webroot'], app)
	else:
		root_app.merge(app)

	session_opts = {
		'session.type': 'cookie',
		'session.validate_key': config['cookieKey'],
		'session.auto': True,
	}

	bottle.run(SessionMiddleware(root_app, session_opts),
		host = config['host'],
		port = config['port'],
		debug = config['debug'],
		reloader = False,
		server = 'cherrypy')

	if scheduler:
		scheduler.stop()

	# Write out default values
	config.write()

def authenticated(func):
    def wrapped(*args, **kwargs):
		if config['password']:
			try:
				beaker_session = request.environ['beaker.session']
			except:
				redirectRelative('/login')

			if beaker_session.get('logged_in', 0):
				valid = True
			else:
				redirectRelative('/login')
		
		return func(*args, **kwargs)
    return wrapped

def render_template(view, extra={}):
	jsAPI = ''
	if config['debug']:
		jsAPI = api.generate_jsapi()

	vars = {
		'apikey'	: config['apikey'] or '',
		'password'	: config['password'],
		'debug'		: config['debug'],
		'jsAPI'		: jsAPI
	}
	vars.update(extra)
	return template(view, vars);

@app.route('/')
def home_page():
	""" Specific redirect as we cannot redirect relatively if the trailing slash is ommitted """
	return """<html><body><script>
	window.location.replace(window.location.href.replace(/\/?$/, '/') + 'devices')
	</script></body></html>"""


@app.route('/login')
def login():
	if config['password']:
		return render_template('login')
	else:
		redirectRelative('/')

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@app.post('/postlogin')
def post_login():
	"""Authenticate users"""
	username = post_get('username')
	password = post_get('password')

	if username == config['username']:
		if check_password_hash(config['password'], password):
			s = bottle.request.environ.get('beaker.session')
			s['logged_in'] = True
			redirectRelative('.')
			return
	
	redirectRelative('/login')

@app.route('/devices')
@authenticated
def devices():
	return render_template('devices')

@app.route('/logout')
def logout():
	s = bottle.request.environ['beaker.session']
	s['logged_in'] = False
	redirectRelative('/login')

@app.route('/api')
@authenticated
def api():
	return render_template('api', {'outputFormat': config['outputFormat']})

@app.route('/config')
@authenticated
def home_page():
	return render_template('config')

@app.route('/scheduler')
@authenticated
def scheduler():
	return render_template('scheduler')

def redirectRelative(url, code=None):
    """ Aborts execution and causes a 303 or 302 redirect, depending on
        the HTTP protocol version. """
    if code is None:
        code = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
	if config['webroot']:
		url = config['webroot'] + url
	if len(url) > 1:
		url = url.rstrip('/').lstrip('/')
    res = bottle.HTTPResponse("", status=code, Location=url)
    if bottle.response._cookies:
        res._cookies = response._cookies
    raise res
	
@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return bottle.static_file(filepath, root=utilities.full_path('/static'))

if __name__ == "__main__":
	main()
