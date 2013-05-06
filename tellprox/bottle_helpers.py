from bottle import *
import json

""" Bottle helper functions """
def raise404():
	raise HTTPError(404, "Not found: " + repr(request.path))

def get_int(key):
	num = request.query.get(key) or ''
	try:
		return int(num)
	except ValueError:
		return num

def get_string(key):
	return request.query.get(key)

def format_response(input, out_format, pretty_print = False):
	if (out_format.lower() == 'xml'):
		#converted = xmlrpclib.dumps(({'vol':'III', 'title':'Magical Unicorn'},))
		converted = "not implemented"
		response.content_type = 'application/xml'
	else:
		converted = json.dumps(input, indent = 4 if pretty_print else None)
		callback_function = request.query.get('callback')
		if callback_function:
			converted = callback_function + '(' + converted + ');'
		
		response.content_type = 'application/json'
	return converted