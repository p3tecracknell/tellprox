
class TASensor(object):
	def __init__(self, config, rawsensor):
		super(TASensor, self).__init__()
		super(TASensor, self).__setattr__('id', str(rawsensor.id))
		super(TASensor, self).__setattr__('raw', rawsensor)
		
		# Create a config entry with default values if one doesn't exist
		sensor_config = config['sensors']
		if not self.id in sensor_config.keys():
			sensor_config[self.id] = {
				'ignore' : 0,
				'name'   : None
			}
			
		super(TASensor, self).__setattr__('config', config)
		super(TASensor, self).__setattr__('snscfg', sensor_config[self.id])
		super(TASensor, self).__setattr__('ignore', sensor_config[self.id]['ignore'])
		super(TASensor, self).__setattr__('name',   sensor_config[self.id]['name'])
	
	def __setattr__(self, name, value):
		if name == 'name':
			self.snscfg['name'] = value
			self.config.write()
		elif name == 'ignore':
			self.snscfg['ignore'] = int(value)
			self.config.write()
		else:
			raise AttributeError(name)
		super(TASensor, self).__setattr__(name, value)