import bottle_helpers as bh

class ConfigAPI(object):
	def __init__(self, api, config):
		self.config = config
		self.api = api
		api.add_route('config', self.route)
	
	def is_section(self, val):
		if not isinstance(val, str):
			print self.config[val].depth
		return False#not isinstance(val, (str, unicode, list, tuple))
		
	def route(self, func):
		if (func == 'getall'):
			return [{k:v} for k, v in self.config.iteritems()
				if not self.is_section(k)]
				
		elif (func == 'get'):
			key = bh.get_string('key')
			if key in self.config:
				return self.config[key]
		bh.raise404()