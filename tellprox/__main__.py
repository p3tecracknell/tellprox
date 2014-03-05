#!/usr/bin/env python

import sys
if sys.version_info < (2, 5):
    print "Sorry, requires Python 2.5, 2.6 or 2.7."
    sys.exit(1)

import json, bottle
import os.path
import httplib, urllib, sys

from api import API
from tellstick import TellstickAPI
from config import ConfigAPI
from scheduler import SchedulerAPI
from bottle import template, redirect, request
from configobj import ConfigObj
from validate import Validator
from beaker.middleware import SessionMiddleware
from werkzeug.security import check_password_hash

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'
ALLJS = './tellprox/static/compiled.js'

config = ConfigObj(CONFIG_PATH, configspec = CONFIG_SPEC)
bottle.TEMPLATE_PATH.insert(0, './tellprox/views')
root_app = bottle.Bottle()
app = bottle.Bottle()
session_opts = {
    'session.type': 'cookie',
	'session.validate_key': 'secret',
    'session.auto': True,
}
api = None

def main():
	global api
	validator = Validator()
	result = config.validate(validator, copy = True)

	if result is False:
		print "Config file validation failed"
		sys.exit(1)
	
	if not os.path.isfile(ALLJS):
		install()

	api = API(app, config)
	TellstickAPI(api, config)
	ConfigAPI(api, config, validator)
	SchedulerAPI(api, config)
	
	if config['webroot']:
		root_app.mount(config['webroot'], app)
	else:
		root_app.merge(app)

	bottle.run(SessionMiddleware(root_app, session_opts),
		host = config['host'],
		port = config['port'],
		debug = config['debug'],
		reloader = config['debug'],
		server = 'cherrypy')

	# Write out default values
	config.write()

def authenticated(func):
    def wrapped(*args, **kwargs):
		valid = False
		if not config['password']:
			valid = True
		else:
			try:
				beaker_session = request.environ['beaker.session']
			except:
				abort(401, "Failed beaker_session in slash")

			if beaker_session.get('logged_in', 0):
				valid = True
			else:
				redirect('/login')
		
		return func(*args, **kwargs)
    return wrapped

def render_template(view, extra=None):
	vars = {
		'apikey'	: config['apikey'] or '',
		'password'	: config['password'],
		'debug'		: config['debug'],
		'jsAPI'		: api.generate_jsapi()
	}
	if extra: vars.update(extra)
	return template(view, vars);

@app.route('/')
def home_page():
	return """<html><body><script>
		window.location.replace(window.location.href.replace(/\/?$/, '/') + 'devices') </script></body></html>"""

@app.route('/login')
def login():
	if config['password']:
		return """<html><body><form method="post" action="postlogin"><input type="text" name="username"/><input type="text" name="password"/><input type="submit"></form></body></html>"""
	else:
		bottle.redirect('/')

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
			bottle.redirect('/devices')
			return
	
	bottle.redirect('/login')

@app.route('/devices')
@authenticated
def devices():
	return render_template('devices')

@app.route('/logout')
def logout():
	s = bottle.request.environ['beaker.session']
	s['logged_in'] = False
	bottle.redirect('/login')

@app.route('/api')
@authenticated
def api():
	return render_template('api', {'outputFormat': config['outputFormat']})

@app.route('/config')
@authenticated
def home_page():
	return render_template('config')

def readfile(path):
	f = open(path, 'r')
	contents = f.read()
	f.close()
	return contents

@app.route('/install')
@authenticated
def install():
	params = urllib.urlencode([
		('js_code', readfile('./tellprox/static/js/jquery-2.1.0.min.js')),
		('js_code', readfile('./tellprox/static/js/jquery.toast.min.js')),
		('js_code', readfile('./tellprox/static/js/bootstrap.min.js')),
		('js_code', readfile('./tellprox/static/js/bootstrap-switch.js')),
		('js_code', readfile('./tellprox/static/js/bootstrap-select.min.js')),
		('js_code', readfile('./tellprox/static/js/helpers.js')),
		('js_code', api.generate_jsapi()),
		('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
		('output_format', 'text'),
		('output_info', 'compiled_code')
	  ])

	# Always use the following value for the Content-type header.
	headers = { "Content-type": "application/x-www-form-urlencoded" }
	conn = httplib.HTTPConnection('closure-compiler.appspot.com')
	conn.request('POST', '/compile', params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	f = open(ALLJS, 'w')
	f.write(data)
	f.close()
	
	return "OK"

@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return bottle.static_file(filepath, root='./tellprox/static')

if __name__ == "__main__":
	main()