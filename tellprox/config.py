import bottle_helpers as bh
from werkzeug.security import generate_password_hash

class ConfigAPI(object):
	def __init__(self, api, config):
		self.config = config
		self.api = api
		api.add_route('config', self.route)
		
	def route(self, func):
		if (func == 'getall'):
			return {k:v for k, v in self.config.iteritems()}
				
		elif (func == 'get'):
			item = bh.get_string('item')
			if not item:
				return { 'error' : 'Item not set' }
			if item in self.config:
				return self.config[item]
		
		elif (func == 'set'):
			item = bh.get_string('item')
			if not item:
				return { 'error' : 'Item not set' }
			if not item in self.config:
				return { 'error' : 'Item not found' }
			value = bh.get_string('value')
			if item == 'password' and not value == '':
				value = generate_password_hash(value)
			self.config[item] = value
			return bh.success_response()
			
		bh.raise404()