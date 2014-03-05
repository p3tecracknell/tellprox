from bottle import *
import bottle_helpers as bh
import tellcore.telldus as td
import time

class SchedulerAPI(object):
	config = None
	core = td.TelldusCore()
	jobs = {}

	def __init__(self, api, config):
		self.config = config
		
		self.jobs = config['jobs']
		
		api.add_route('scheduler', {
			'joblist': {
				'fn': self.joblist
			},
			'jobinfo': {
				'fn': self.jobinfo,
				'inputs': [
					{ 'name': 'id', 'type': 'string', 'description': 'Jobs unique identifier' }
				]
			},
			'setjob': {
				'fn': self.setjob,
				'inputs': [
				{ 'name': 'id', 'type': 'string', 'description': 'The job id, when updating an existing job' },
				{ 'name': 'deviceId', 'type': 'string', 'description': 'The device id to schedule. Only valid when creating a new job' },
				{ 'name': 'method', 'type': 'string', 'description': 'What to do when the schdule runs. This should be any of the method constants' },
				{ 'name': 'methodValue', 'type': 'string', 'description': 'Only required for methods that requires this.' },
				{ 'name': 'type', 'type': 'dropdown', 'description': 'This can be \'time\', \'sunrise\' or \'sunset\'', 'options': ['time', 'sunrise', 'sunset'] },
				{ 'name': 'hour', 'type': 'string', 'description': 'A value between 0-23', 'default': time.strftime("%H") },
				{ 'name': 'minute', 'type': 'string', 'description': 'A value between 0-59' },
				{ 'name': 'offset', 'type': 'string', 'description': 'A value between -1439-1439. This is only used when type is either \'sunrise\' or \'sunset\'' },
				{ 'name': 'randomInterval', 'type': 'string', 'description': 'Number of minutes after the specified time to randomize.' },
				{ 'name': 'retries', 'type': 'string', 'description': 'If the client is offline, this specifies the number of times to retry executing the job before consider the job as failed.' },
				{ 'name': 'retryInterval', 'type': 'string', 'description': 'The number if minutes between retries. Example: If retries is 3 and retryInterval is 5 the scheduler will try executing the job every five minutes for fifteen minutes.' },
				{ 'name': 'reps', 'type': 'string', 'description': 'Number of times to resend the job to the client, for better reliability' },
				{ 'name': 'active', 'type': 'dropdown', 'description': 'Is the job active or paused?', 'options': ['1|1 (active)', '0|0 (paused)'] },
				{ 'name': 'weekdays', 'type': 'dropdown-multiple', 'description': 'A comma separated list of weekdays. 1 is monday. Example: 2,3,4', 'options': ['1|1 (Monday)', '2|2 (Tuesday)', '3|3 (Wednesday)', '4|4 (Thursday)', '5|5(Friday)', '6|6(Saturday)', '7|7(Sunday)'] }
				]
			}
		})

	def joblist(self, func):
		"""Job list"""
		return { 'job': [
			job for id, job in self.jobs.iteritems()
		]}
	
	def jobinfo(self, func, id):
		if id and id in self.jobs:
			return self.jobs[id]
		return { 'error' : 'The request job was not found' }
		
	def setjob(self, func, id, deviceId, method, methodValue, type, hour,
		minute, offset, randomInterval, retries, retryInterval, reps, active, weekdays):
		
		if id:
			try:
				id = int(id)
			except ValueError:
				id = None
	
		# If no ID is provided, find the next available
		if id is None == 0 or id == 0:
			keys = self.jobs.keys()
			if len(keys) == 0:
				id = 1
			else:
				id = max([int(k) for k in keys]) + 1
		id = str(id)
			
		nextRunTime = "1388318160" #TODO

		self.jobs[id] = {
			'id'             : id,
			'deviceId'       : deviceId,
			'method'         : method,
			'methodValue'    : methodValue,
			'nextRunTime'    : nextRunTime,
			'type'           : type,
			'hour'           : hour,
			'minute'         : minute,
			'offset'         : offset,
			'randomInterval' : randomInterval,
			'retries'        : retries or 3,
			'retryInterval'  : retryInterval or 5,
			'reps'           : reps or 1,
			'active'         : active or 1,
			'weekdays'       : weekdays
		}
		self.config.write()
		return { 'id' : id, 'nextRunTime': nextRunTime }