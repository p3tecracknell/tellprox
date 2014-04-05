from bottle import *
from operator import itemgetter
from scheduler import Scheduler
import bottle_helpers as bh
import tellcore.telldus as td
import time
import bottle_helpers as bh

class SchedulerAPI(object):
	config = None
	core = td.TelldusCore()
	jobs = {}
	schedulerThread = None

	def __init__(self, api, config, scheduler):
		self.config = config
		
		self.jobs = config['jobs']
		self.schedulerThread = scheduler

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
				{ 'name': 'id', 'type': 'int', 'description': 'The job id, when updating an existing job' },
				{ 'name': 'deviceId', 'type': 'string', 'description': 'The device id to schedule. Only valid when creating a new job' },
				{ 'name': 'method', 'type': 'string', 'description': 'What to do when the schedule runs. This should be any of the method constants' },
				{ 'name': 'methodValue', 'type': 'int', 'description': 'Only required for methods that requires this.' },
				{ 'name': 'type', 'type': 'dropdown', 'description': 'This can be \'time\', \'sunrise\' or \'sunset\'', 'options': ['time', 'sunrise', 'sunset'] },
				{ 'name': 'hour', 'type': 'int', 'description': 'A value between 0-23'},#, 'default': time.strftime("%H") },
				{ 'name': 'minute', 'type': 'int', 'description': 'A value between 0-59' },
				{ 'name': 'offset', 'type': 'int', 'description': 'A value between -1439-1439. This is only used when type is either \'sunrise\' or \'sunset\'' },
				{ 'name': 'randomInterval', 'type': 'int', 'description': 'Number of minutes after the specified time to randomize.' },
				{ 'name': 'retries', 'type': 'int', 'description': 'If the client is offline, this specifies the number of times to retry executing the job before consider the job as failed.' },
				{ 'name': 'retryInterval', 'type': 'int', 'description': 'The number of minutes between retries. Example: If retries is 3 and retryInterval is 5 the scheduler will try executing the job every five minutes for fifteen minutes.' },
				{ 'name': 'reps', 'type': 'int', 'description': 'Number of times to resend the job to the client, for better reliability' },
				{ 'name': 'active', 'type': 'dropdown', 'description': 'Is the job active or paused?', 'options': ['1|1 (active)', '0|0 (paused)'] },
				{ 'name': 'weekdays', 'type': 'dropdown-multiple', 'description': 'A comma separated list of weekdays. 1 is monday. Example: 2,3,4', 'options': ['1|1 (Monday)', '2|2 (Tuesday)', '3|3 (Wednesday)', '4|4 (Thursday)', '5|5(Friday)', '6|6(Saturday)', '7|7(Sunday)'] }
				]
			},
			'removejob': {
				'fn': self.removejob,
				'inputs': [{ 'name': 'id', 'type': 'string', 'description': 'The job id' }]
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
	
	def calcNextRunTime(self, job):
		hour = int(job['hour'])
		minute = int(job['minute'])
		weekdays = job['weekdays']
		
		currentTime = dt.datetime.now().replace(second=0, microsecond=0)
		
		def calcRunTime(weekday):
			newDate = currentTime.replace(hour = hour, minute = minute, second = 0) + timedelta(days=weekday)
			if newDate < currentTime:
				newDate += timedelta(days=7)
			return newDate

		# Convert days into 0 based integers
		daysToRun = map(lambda d: int(d) - 1, weekdays.split(','))
		allDays = [calcRunTime(day) for day in daysToRun]
		allDays.sort() 
		if not allDays:
			return None
		
		nextRunTime = allDays[0]
		return self.dateTimeToEpoch(nextRunTime)
		
	def dateTimeToEpoch(self, timeObj):
		return int(time.mktime(timeObj.timetuple()))
	
	def removejob(self, func, id):
		if id in self.jobs:
			del self.jobs[id]
			self.restartSchedulerThread()
		return { "status" : "OK" }
	
	def restartSchedulerThread(self):
		if self.schedulerThread:
			self.schedulerThread.stop()
		self.schedulerThread.start(self.config)
	
	def setjob(self, func, id, deviceId, method, methodValue, type, hour,
		minute, offset, randomInterval, retries, retryInterval, reps, active, weekdays):
	
		# If no ID is provided, find the next available
		if id is None or id == 0:
			keys = self.jobs.keys()
			if len(keys) == 0:
				id = 1
			else:
				id = max([int(k) for k in keys]) + 1

		id = str(id)

		newJob = {
			'id'             : id,
			'deviceId'       : deviceId,
			'method'         : method or 1,
			'methodValue'    : methodValue or 0,
			'type'           : type,
			'hour'           : hour or 0,
			'minute'         : minute or 0,
			'offset'         : offset or 0,
			'randomInterval' : randomInterval,
			'retries'        : retries or 3,
			'retryInterval'  : retryInterval or 5,
			'reps'           : reps or 1,
			'active'         : active or '1',
			'weekdays'       : weekdays
		}
		
		self.jobs[id] = newJob
		bh.calcNextRunTime(newJob)
		
		self.restartSchedulerThread()
		self.config.write()
		return { 'id' : id, 'nextRunTime': newJob['nextRunTime'] }