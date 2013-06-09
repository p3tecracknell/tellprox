from bottle import *
import xml.etree.cElementTree as ET
from xml.dom import minidom
import json

""" Bottle helper functions """
def raise404():
	raise HTTPError(404, "Not found: " + repr(request.path))

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
		#converted = "not implemented"
		converted = prettify(root)
		response.content_type = 'application/xml'
	else:
		converted = json.dumps(input, indent = 4 if pretty_print else None)
		callback_function = request.query.get('callback')
		if callback_function:
			converted = callback_function + '(' + converted + ');'
		
		response.content_type = 'application/json'
	return converted

def prettify(elem):
	"""Return a pretty-printed XML string for the Element.
		"""
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
				#if tag.startswith('@'):
				parent.attrib[str(tag)] = str(child)
				#else: 
				#	elem = ET.Element(tag)
				#	parent.append(elem)
				#	_convert_dict_to_xml_recurse(elem, child, listnames)
	elif not dictitem is None:
		parent.text = unicode(dictitem)
	