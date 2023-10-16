"""
Copyright 2023 Hervé Leleu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re

# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# CLASS
# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

class xml_parser:
	'''get the elements, extract and output data & status'''
	def __init__(self):
		pass
	
	def parse_xml(self, tag, element, action):
		'''run a function matching the OOXML tag and return a dictionary
		   - type: style, insertion, text, etc.
		   - content: element.text, attribute, None, etc.
		   - track: True or False '''
		try:
			parser_output = getattr(self, tag)(element, action)
			#when the text content is None, make it an empty string
			if parser_output == None:
				parser_output = {"type": "", "content": "", "track": False}
		except:
			#if the tag has no matching function, make the text an empty string
			parser_output = {"type": "", "content": "", "track": False}
		finally:
			return parser_output
	
	# ======================================================== #
	# the following functions are matching elements from OOXML #
	# ======================================================== #
	
	#Note: VSDX has no ancestry tracking

	# # # masters.xml
	def Masters(self, element, action):
		return {"type": "masters", "content": f"", "track": False}
	
	def Master(self, element, action):
		tag_attributes = ""
		if action == "start":
			tag_attributes =_extract_attrib(element.attrib,["Name", "NameU", "Prompt"])
			return {"type": "master", "content": f"<div{tag_attributes}>", "track": False}
		else:
			return {"type": "master", "content": "</div>", "track": False}

	# # # master%n.xml
	def MasterContents(self, element, action):
		return {"type": "master_contents", "content": "", "track": False}

	# # # pages.xml
	def Pages(self, element, action):
		return {"type": "pages", "content": "", "track": False}
	
	def Page(self, element, action):
		tag_attributes = ""
		if action == "start":
			tag_attributes =_extract_attrib(element.attrib,["Name", "NameU", "Prompt"])
			return {"type": "page", "content": f"<div{tag_attributes}>", "track": False}
		else:
			return {"type": "page", "content": "</div>", "track": False}

	# # # page%n.xml
	def PageContents(self, element, action):
		return {"type": "page_contents", "content": "", "track": False}

	# # # standard paragraph content
	def Shapes(self, element, action):
		pass

	def Shape(self, element, action):
		tag_attributes = ""
		if action == "start":
			tag_attributes =_extract_attrib(element.attrib,["Name", "NameU", "Prompt"])
			if len(tag_attributes) > 0:
				return {"type": "shape", "content": f"<span{tag_attributes}></span>", "track": False}
			else:
				return {"type": "shape", "content": None, "track": False}	
		else:
			return {"type": "shape", "content": None, "track": False}
	
	def Section(self, element, action):
		pass

	def Row(self, element, action):
		pass

	def Cell(self, element, action):
		#see https://learn.microsoft.com/en-us/openspecs/sharepoint_protocols/ms-vsdx/c31ebb48-e792-4308-8bc0-ebcba281ce20
		content = ""
		tag_attributes = ""
		if action == "start":
			if element.attrib.get("U", None) == "STR":
				content = element.attrib.get("V", "")
			if element.text != None:
				content = element.text
			tag_attributes =_extract_attrib(element.attrib,["ShapeKeywords", "Name", "NameU", "Comment", "Description"])
			if len(tag_attributes + content) > 0:
				return {"type": "cell", "content": f"<p{tag_attributes}>{content}</p>", "track": False}

	def Text(self, element, action):
		content = ""
		if action == "start":
			if element.text != None:
				content = element.text.replace("\n", "<br />")
				return {"type": "text", "content": f"<p>{content}</p>", "track": False}

# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# STANDALONE FUNCTIONS
# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

def _extract_attrib(a_dict, n_list):
	'''
	input: dictionnary with attributes from element, list of attributes to extract
	output: string with the values
	'''
	temp_a = {k:a_dict.get(k, None) for k in n_list if a_dict.get(k, None) is not None}
	a_str = ""
	if len(temp_a) > 0:
		for k in temp_a:
			a_str += f" {k}=\'{temp_a.get(k)}\'"

	return (a_str)