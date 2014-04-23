import os, urllib, httplib

def full_path(sub_path):
    return os.path.dirname(__file__) + sub_path

def readfile(sub_path):
	f = open(full_path(sub_path), 'r')
	contents = f.read()
	f.close()
	return contents

#TODO make this generic
def generateCompiledJS(jsApi, outputFile):
	params = urllib.urlencode([
		('js_code', readfile('/static/js/jquery-2.1.0.min.js')),
		('js_code', readfile('/static/js/jquery.toast.min.js')),
		('js_code', readfile('/static/js/bootstrap.min.js')),
		('js_code', readfile('/static/js/bootstrap-switch.js')),
		('js_code', readfile('/static/js/bootstrap-select.min.js')),
		('js_code', readfile('/static/js/knockout-3.1.0.js')),
		('js_code', readfile('/static/js/helpers.js')),
		('js_code', jsApi),
		('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
		('output_format', 'text'),
		('output_info', 'compiled_code')
	  ])

	# Always use the following value for the Content-type header.
	headers = { "Content-type": "application/x-www-form-urlencoded" }
	conn = httplib.HTTPConnection('closure-compiler.appspot.com')
	conn.request('POST', '/compile', params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	#todo helper method
	f = open(outputFile, 'w')
	f.write(data)
	f.close()
