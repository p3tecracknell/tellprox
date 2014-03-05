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
				'fn': self.get,
				'inputs': [
					{ 'name': 'item', 'type': 'string', 'description': 'Config item name' }
				]
			},
			'set': {
				'fn': self.set,
				'inputs': [
					{ 'name': 'item', 'type': 'string', 'description': 'Item key' },
					{ 'name': 'value', 'type': 'string', 'description': 'New value' },
				]
			}
		})
		
	def getall(self, func):
		return { k:v for k, v in self.config.iteritems() }
	
	def get(self, func, item):
		if not item:
			return { 'error' : 'Item not set' }
		if item in self.config:
			return self.config[item]
	
	def set(self, func, item, value):
		if not item:
			return { 'error' : 'Item not set' }
		if not item in self.config:
			return { 'error' : 'Item not found' }
		if item == 'password' and value:
			value = generate_password_hash(value)

		self.config[item] = value
		result = self.config.validate(self.validator)
		return bh.success_response()