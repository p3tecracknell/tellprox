from bottle import *
from xml.dom import minidom
import xml.etree.cElementTree as ET
import json
import datetime as dt
import sys

_startup_cwd = os.getcwd()

""" Bottle helper functions """
def raise404():
	raise HTTPError(404, "Not found: " + repr(request.path))

def get_type(key, type):
	if type == 'int':
		return get_int(key)
	else:
		return get_string(key)

def get_int(key):
	num = get_string(key) or ''
	try:
		return int(num)
	except ValueError:
		return num

def get_string(key):
	return request.query.get(key) or request.forms.get(key)

def format_response(input, out_format, root_tag, pretty_print = False):
	if (out_format.lower() == 'xml'):
		root = ET.Element(root_tag)
		_convert_dict_to_xml_recurse(root, input, {})
		converted = prettify(root)
		response.content_type = 'application/xml'
	else:
		# Crude. Need to loop through properly and rip out keys starting with @
		if isinstance(input, dict):
			for child in input.values():
				if isinstance(child, list):
					for index in range(len(child)):
						if isinstance(child[index], dict):
							child[index] = hide_attribute(child[index])

		converted = json.dumps(input, indent = 4 if pretty_print else None)
		callback_function = request.query.get('callback')
		if callback_function:
			converted = callback_function + '(' + converted + ');'
		
		response.content_type = 'application/json'
	return converted

def success_response():
	return { 'status': 'success' } 

def set_attribute(dictionary):
	return dict(("@" + k, v) for k, v in dictionary.items())

def hide_attribute(dictionary):
	return dict((k[1:] if k.startswith('@') else k, v) for k, v in dictionary.items())

def prettify(elem):
	"""Return a pretty-printed XML string for the Element."""
	rough_string = ET.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

def _convert_dict_to_xml_recurse(parent, dictitem, listnames):
	"""Helper Function for XML conversion."""
	# we can't convert bare lists
	assert not isinstance(dictitem, list)

	if isinstance(dictitem, dict):
		for (tag, child) in sorted(dictitem.iteritems()):
			if isinstance(child, list):
				for listchild in child:
					elem = ET.Element(tag)
					parent.append(elem)
					_convert_dict_to_xml_recurse(elem, listchild, listnames)
			else:
				if tag.startswith('@'):
					parent.attrib[str(tag[1:])] = str(child)
				else: 
					elem = ET.Element(tag)
					parent.append(elem)
					_convert_dict_to_xml_recurse(elem, child, listnames)
	elif not dictitem is None:
		parent.text = unicode(dictitem)

			
def calcNextRunTime(job):
	hour = int(job['hour'])
	minute = int(job['minute'])
	weekdays = job['weekdays']
	
	currentTime = dt.datetime.now().replace(second=59, microsecond=0)
	currentWeekday = currentTime.weekday()
	
	def calcRunTime(weekday):
		weekdayOffset = weekday - currentWeekday
		newDate = currentTime.replace(hour = hour, minute = minute, second = 0) + dt.timedelta(days=weekdayOffset)
		if newDate < currentTime:
			newDate += dt.timedelta(days=7)
		return newDate

	# Convert days into 0 based integers
	daysToRun = (int(d) - 1 for d in weekdays.split(','))
	allDays = [calcRunTime(day) for day in daysToRun]
	allDays.sort() 
	if allDays:
		nextRunTime = allDays[0]
		nextRunTime = dateTimeToEpoch(nextRunTime)
	else:
		nextRunTime = None
	job['nextRunTime'] = nextRunTime

		
def dateTimeToEpoch(timeObj):
	return int(time.mktime(timeObj.timetuple()))
	
def shutdown():
	return "not implemented"
	
def restart():
	args = sys.argv[:]

	args.insert(0, sys.executable)
	if sys.platform == 'win32':
		args = ['"%s"' % arg for arg in args]

	os.chdir(_startup_cwd)
	os.execv(sys.executable, args)
