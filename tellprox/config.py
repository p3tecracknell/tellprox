import bottle_helpers as bh
from werkzeug.security import generate_password_hash

class ConfigAPI(object):
	def __init__(self, api, config, validator):
		self.api = api
		self.config = config
		self.validator = validator
		api.add_route('config', {
			'getall': {
				'fn': self.getall
			},
			'get': {
				'fn': self.get
			},
			'set': {
				'fn': self.set
			}
		})
		
	def getall(self, func):
		return { k:v for k, v in self.config.iteritems() }
	
	def get(self, func):
		item = bh.get_string('item')
		if not item:
			return { 'error' : 'Item not set' }
		if item in self.config:
			return self.config[item]
	
	def set(self, func):
		item = bh.get_string('item')
		if not item:
			return { 'error' : 'Item not set' }
		if not item in self.config:
			return { 'error' : 'Item not found' }
		value = bh.get_string('value')
		if item == 'password' and not value == '':
			value = generate_password_hash(value)

		self.config[item] = value
		result = self.config.validate(self.validator)
		return bh.success_response()