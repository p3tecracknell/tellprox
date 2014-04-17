from UserDict import IterableUserDict
from configobj import ConfigObj

class ConfigObserver(ConfigObj):
	def __init__(self, *args, **kw):
		self.observers = []
		self.observeKeys = {}
		
		self.validator = None
		self.validating = False
		super(ConfigObserver, self).__init__(*args, **kw)
	
	def setValidator(self, validator):
		self.validator = validator
		
	def observe(self, observer):
		self.observers.append(observer)
		
	def observeKey(self, key, observer):
		if not key in self.observeKeys:
			self.observeKeys[key] = []
		self.observeKeys[key].append(observer)
	
	def notify(self, key):
		for o in self.observers:
			o.notify(self, key)
	
	def notifyKey(self, key):
		self.notify(key)
		if key in self.observeKeys:
			for o in self.observeKeys[key]:
				o.notify(self, key)

	def __setitem__(self, key, value, unrepr = False):
		currentValue = ''
		if key in self:
			currentValue = self[key]

		ConfigObj.__setitem__(self, key, value, unrepr)
		if currentValue == value: return
		
		result = True
		if self.validator:
			if not self.validating:
				self.validating = True
				result = self.validate(self.validator, preserve_errors = True)
	
		if result and self.validating:
			self.notifyKey(key)
			self.validating = False
		