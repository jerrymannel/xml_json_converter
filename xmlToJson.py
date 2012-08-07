"""
Name     : xmltoJson.py
Author   : Jerry M. Reghunadh
Version  : 1.0
Comment  : XML to Badgerfish JSON converter
Badgerfish convention -> http://badgerfish.ning.com/
"""

import xml.sax
import json

"Class for SAX ContentHandle"
class XMLSAXContentHandler (xml.sax.ContentHandler):
	
	_key = []
	data = {}
	_currData = {}
	_prevData = []
	_namespace = {}
	
	def __init__(self,):
		xml.sax.ContentHandler.__init__(self)
		self._key = []
		self.data = {}
		self._currData = {}
		self._prevData = []
		self._namespace = {}
	
	def startElement(self, name, attrs):
		if len(self.data) == 0 :
			self.data[name] = {}
			self._currData = self.data
			self._key.append(name)
			self._prevData.append(self.data)
		else:
			if self._key[len(self._key) - 1] not in self._currData.keys():
				self._currData[self._key[len(self._key) - 1]] = {}
			if name not in self._currData[self._key[len(self._key) - 1]].keys():
				self._currData[self._key[len(self._key) - 1]][name] = {}
			self._prevData.append(self._currData)
			self._currData = self._currData[self._key[len(self._key) - 1]]
			if len(self._namespace) > 0:
				self._currData[name]["@xmlns"] = self._namespace
			self._key.append(name)
		if( len(attrs) > 0 ):
			for _key in attrs.getNames():
				if _key[0:5] == "xmlns":
					if "@xmlns" not in self._currData[name].keys():
						self._currData[name]["@xmlns"] = {}
					if len(_key) == 5:
						self._currData[name]["@xmlns"]["$"] = attrs.getValue(_key)
					else:
						self._currData[name]["@xmlns"][_key[6:len(_key)]] = attrs.getValue(_key)
					self._namespace = self._currData[name]["@xmlns"]
				else:
					self._currData[name]["@"+_key] = attrs.getValue(_key)
	
	def characters(self, content):
		if content != " ":
			if self._key[len(self._key) - 1] not in self._currData.keys():
				self._currData[self._key[len(self._key) - 1]] = {}
			if "$" not in self._currData[self._key[len(self._key) - 1]].keys():
				self._currData[self._key[len(self._key) - 1]]["$"] = content
			else:
				if len(self._currData[self._key[len(self._key) - 1]]) == 1:
					temp = self._currData[self._key[len(self._key) - 1]]
					self._currData[self._key[len(self._key) - 1]] = []
					self._currData[self._key[len(self._key) - 1]].append(temp)
				temp = {}
				temp["$"] = content
				self._currData[self._key[len(self._key) - 1]].append(temp)
			
	def endElement(self, name):
		self._key.pop()
		self._currData = self._prevData.pop()

"Call this function after importing the package."
def to_json(xmlString):
	handler = XMLSAXContentHandler()
	xml.sax.parseString(xmlString, handler)
	return json.dumps(handler.data)
