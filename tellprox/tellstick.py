#!/usr/bin/env python

from ctypes import util, cdll, c_char_p
from sys import platform
import ctypes

# Device methods
TELLSTICK_TURNON = 1
TELLSTICK_TURNOFF = 2
TELLSTICK_BELL = 4
TELLSTICK_TOGGLE = 8
TELLSTICK_DIM = 16
TELLSTICK_LEARN = 32
TELLSTICK_EXECUTE = 64
TELLSTICK_UP = 128
TELLSTICK_DOWN = 256
TELLSTICK_STOP = 512

# Sensor value types
TELLSTICK_TEMPERATURE = 1
TELLSTICK_HUMIDITY = 2

# Error codes
TELLSTICK_SUCCESS = 0
TELLSTICK_ERROR_BROKEN_PIPE = -9
TELLSTICK_ERROR_COMMUNICATING_SERVICE = -10
TELLSTICK_ERROR_COMMUNICATION = -5
TELLSTICK_ERROR_CONNECTING_SERVICE = -6
TELLSTICK_ERROR_DEVICE_NOT_FOUND = -3
TELLSTICK_ERROR_METHOD_NOT_SUPPORTED = -4
TELLSTICK_ERROR_NOT_FOUND = -1
TELLSTICK_ERROR_PERMISSION_DENIED = -2
TELLSTICK_ERROR_SYNTAX = -8
TELLSTICK_ERROR_UNKNOWN = -99
TELLSTICK_ERROR_UNKNOWN_RESPONSE = -7

# Device typedef
TELLSTICK_TYPE_DEVICE = 1
TELLSTICK_TYPE_GROUP = 2
TELLSTICK_TYPE_SCENE = 3

# Device changes
TELLSTICK_DEVICE_ADDED = 1
TELLSTICK_DEVICE_CHANGED = 2
TELLSTICK_DEVICE_REMOVED = 3
TELLSTICK_DEVICE_STATE_CHANGED = 4

# Change types
TELLSTICK_CHANGE_NAME = 1
TELLSTICK_CHANGE_PROTOCOL = 2
TELLSTICK_CHANGE_MODEL = 3
TELLSTICK_CHANGE_METHOD = 4
TELLSTICK_CHANGE_AVAILABLE = 5
TELLSTICK_CHANGE_FIRMWARE = 6

TELLSTICK_CONTROLLER_TELLSTICK = 1
TELLSTICK_CONTROLLER_TELLSTICK_DUO = 2
TELLSTICK_CONTROLLER_TELLSTICK_NET = 3

class TellStick(object):
	def loadlibrary(self, libraryname=None):
		if libraryname == None:
			if platform == "darwin" or platform == "win32":
				libraryname = "TelldusCore"
			elif platform == "linux2":
				libraryname = "telldus-core"
			else:
				libraryname = "TelldusCore"
			ret = util.find_library(libraryname)
		else:
			ret = libraryname
		
		if ret == None:
			return (None, libraryname)

		global libtelldus
		if platform == "win32":
			libtelldus = windll.LoadLibrary(ret)
		else:
			libtelldus = cdll.LoadLibrary(ret)
		libtelldus.tdGetName.restype = c_char_p
		libtelldus.tdLastSentValue.restype = c_char_p
		libtelldus.tdGetProtocol.restype = c_char_p
		libtelldus.tdGetModel.restype = c_char_p
		libtelldus.tdGetErrorString.restype = c_char_p
		libtelldus.tdLastSentValue.restype = c_char_p

		return ret, libraryname

	def add(self, name, protocol, model):
		newId = libtelldus.tdAddDevice()
		if (newId < 0):
			return { "error" : "Unable to add device" }
		resp = libtelldus.tdSetName(newId, name)
		if (resp is False):
			return { "error" : "Unable to set name" }
		
		resp = libtelldus.tdSetProtocol(newId, protocol)
		if (resp is False):
			return { "error" : "Unable to set protocol" }
			
		resp = libtelldus.tdSetModel(newId, model)
		if (resp is False):
			return { "error" : "Unable to set model" }
		
		return self.determine_response(TELLSTICK_SUCCESS)

	def remove(self, id):
		response = libtelldus.tdRemoveDevice(id)
		
		modified_response = TELLSTICK_SUCCESS
		if (response == 0):
			modified_response = TELLSTICK_ERROR_DEVICE_NOT_FOUND
		
		return self.determine_response(modified_response, id)

	def bell(self, id):
		return self.command(id, TELLSTICK_BELL)

	def learn(self, id):
		return self.command(id, TELLSTICK_LEARN)

	def execute(self, id):
		return self.command(id, TELLSTICK_EXECUTE)

	def up(self, id):
		return self.command(id, TELLSTICK_UP)

	def down(self, id):
		return self.command(id, TELLSTICK_DOWN)
	
	def stop(self, id):
		return self.command(id, TELLSTICK_STOP)

	def command(self, id, method, value=''):
		if (method == TELLSTICK_TURNON):
			response = libtelldus.tdTurnOn(id)
		elif (method == TELLSTICK_TURNOFF):
			response = libtelldus.tdTurnOff(id)
		elif (method == TELLSTICK_BELL):
			response = libtelldus.tdBell(id)
		elif (method == TELLSTICK_DIM):
			response = libtelldus.tdDim(id, value)
		elif (method == TELLSTICK_LEARN):
			response = libtelldus.tdLearn(id)
		elif (method == TELLSTICK_EXECUTE):
			response = libtelldus.tdExecute(id)
		elif (method == TELLSTICK_UP):
			response = libtelldus.tdUp(id)
		elif (method == TELLSTICK_DOWN):
			response = libtelldus.tdDown(id)
		elif (method == TELLSTICK_STOP):
			response = libtelldus.tdStop(id)
		else:
			response = TELLSTICK_ERROR_METHOD_NOT_SUPPORTED
		
		return self.determine_response(response, id, method)

	def device_type_to_string(self, id):
		if (id == TELLSTICK_TYPE_DEVICE):
			typeText = 'device'
		elif (id == TELLSTICK_TYPE_GROUP):
			typeText = 'group'
		else:
			typeText = 'scene'
		return typeText

	def read_device(self, identity, supportedMethods, getExtras = False):
		methods = libtelldus.tdMethods(identity, supportedMethods)
		lastcmd = libtelldus.tdLastSentCommand(identity, methods)
		lastSentValue = libtelldus.tdLastSentValue(identity)

		info = {
			'id': identity,
			'name': libtelldus.tdGetName(identity),
			'state': lastcmd,
			'statevalue': lastSentValue,
			'methods': methods,
			'type': self.device_type_to_string(libtelldus.tdGetDeviceType(identity)),
			'online': 1,
			'editable': 0
		}
		
		if (getExtras is True):
			info['protocol'] = libtelldus.tdGetProtocol(identity)
			info['model'] = libtelldus.tdGetModel(identity)
			info['parameter'] = []
		
		return info
	
	def on(self, id):
		return self.command(id, TELLSTICK_TURNON)
		
	def off(self, id):
		return self.command(id, TELLSTICK_TURNOFF)

	def dim(self, id, dimlevel):
		return self.command(id, TELLSTICK_DIM, dimlevel)

	def determine_response(self, cmdresp, id = '', method = ''):
		if (cmdresp == TELLSTICK_SUCCESS):
			return { "status":"success" }
		else:
			id = str(id)
			method = str(method)
			if (cmdresp == TELLSTICK_ERROR_DEVICE_NOT_FOUND):
				return { "error" : "Device " + "\"" + id + "\" not found!" }
			elif (cmdresp == TELLSTICK_ERROR_BROKEN_PIPE):
				return { "error" : "Broken pipe" }
			elif (cmdresp == TELLSTICK_ERROR_COMMUNICATING_SERVICE):
				return { "error" : "Communicating service" }
			elif (cmdresp == TELLSTICK_ERROR_COMMUNICATION):
				return { "error" : "Communication" }
			elif (cmdresp == TELLSTICK_ERROR_CONNECTING_SERVICE):
				return { "error" : "Cannot connect to service" }
			elif (cmdresp == TELLSTICK_ERROR_METHOD_NOT_SUPPORTED):
				return { "error" : "Device \"" + id + "\" does not support method \"" + method + "\""}
			elif (cmdresp == TELLSTICK_ERROR_NOT_FOUND):
				return { "error" : "Not found" }
			elif (cmdresp == TELLSTICK_ERROR_PERMISSION_DENIED):
				return { "error" : "Permission denied" }
			elif (cmdresp == TELLSTICK_ERROR_SYNTAX):
				return { "error" : "Syntax error" }
			else:
				return { "error" : "Unknown response" }
	
	def devices(self, supportedMethods):
		numDevices = libtelldus.tdGetNumberOfDevices()
		return [self.read_device(libtelldus.tdGetDeviceId(i), supportedMethods)
				  for i in xrange(0, numDevices)]