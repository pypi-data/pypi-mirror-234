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
	def document(self, element, action):
		pass
	
	def hdr(self, element, action): #Headers
		pass
	
	def ftr(self, element, action): #Footers
		pass
	
	def footnotes(self, element, action):
		pass
	
	def endnotes(self, element, action):
		pass
		
	def sdt(self, element, action): #TOC
		pass
	
	def fldSimple(self, element, action): #Index or Table of figures, Table of tables, etc.
		pass
	
	def p(self, element, action):
		if action == "start":
			return {"type": "paragraph", "content": "<p>", "track": True}
		else:
			return {"type": "paragraph", "content": "</p>", "track": True}
		
	def pPr(self, element, action):
		return {"type": None, "content": None, "track": True}
	
	def pStyle(self, element, action):
		#extract paragraph style
		return {"type": None, "content": None, "track": False}
	
	def r(self, element, action):
		return {"type": None, "content": None, "track": True}
	
	def rPr(self, element, action):
		return {"type": None, "content": None, "track": True}
		#if action == "start":
		#	return {"type": None, "content": "<span class='rPr'>", "track": True}
		#else:
		#	return {"type": None, "content": "</span>", "track": True}
	
	def ins(self, element, action):
		content = ""
		if action == "start":
			date = ""
			author = ""
			date = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date")
			author = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author")
			author = author.replace("'", "_")
			content = f"<insertion date='{date}' author='{author}'>"
		else:
			content = "</insertion>"
		return {"type": "insertion", "content": content, "track": True}
		
	def t(self, element, action):
		content = ""
		if action == "start":
			if element.text != None:
				preserve = element.attrib.get("{http://www.w3.org/XML/1998/namespace}space")
				if preserve == "preserve":
					content = element.text
				else:
					content = element.text.strip()
			return {"type": "text", "content": content, "track": False}
			
	def del_tag(self, element, action):
		'''note: the original tag in OOXML is del, but it was changed because this is a keyword in Python'''
		content = ""
		if action == "start":
			date = ""
			author = ""
			date = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date")
			author = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author")
			author = author.replace("'", "_")
			content = f"<deletion date='{date}' author='{author}'>"
		else:
			content = "</deletion>"
		return {"type": "deletion", "content": content, "track": True}
			
	def delText(self, element, action):
		content = ""
		if action == "start":
			preserve = element.attrib.get("{http://www.w3.org/XML/1998/namespace}space")
			if preserve == "preserve":
				content = element.text
			else:
				content = element.text.strip()
		return {"type": "deletion", "content": content, "track": True}

	def moveFrom(self, element, action):
		content = ""
		if action == "start":
			date = ""
			author = ""
			date = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date")
			author = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author")
			author = author.replace("'", "_")
			content = f"<deletion date='{date}' author='{author}'>"
		else:
			content = "</deletion>"
		return {"type": "deletion", "content": content, "track": True}
	
	def moveTo(self, element, action):
		content = ""
		if action == "start":
			date = ""
			author = ""
			date = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date")
			author = element.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author")
			author = author.replace("'", "_")
			content = f"<insertion date='{date}' author='{author}'>"
		else:
			content = "</insertion>"
		return {"type": "insertion", "content": content, "track": True}		

	def br(self, element, action):
		if action == "start":
			return {"type": "entity", "content": "\n", "track": False}
	
	def cr(self, element, action):
		if action == "start":
			return {"type": "entity", "content": "\n", "track": False}
	
	def tab(self, element, action):
		if action == "start":
			return {"type": "entity", "content": " " * 4, "track": False}
	
	def ptab(self, element, action):
		if action == "start":
			return {"type": "entity", "content": " " * 4, "track": False}

	def noBreakHyphen(self, element, action):
		if action == "start":
			return {"type": "entity", "content": "-", "track": False}
	
	def softHyphen(self, element, action):
		if action == "start":
			return {"type": "entity", "content": "-", "track": False}
	
	#Fallback for older Word versions
	def Fallback(self, element, action):
		content = ""
		if action == "start":
			content = "<!--"
		else:
			content = "-->"
		return {"type": "commented", "content": content, "track": True}
