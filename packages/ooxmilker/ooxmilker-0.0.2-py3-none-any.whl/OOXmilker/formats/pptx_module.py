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
		#discard placeholder content when coming from Master Slides
		self.ms_flag = False #flag for Master Slide
		self.ph_flag = False #flag for a placeholder
	
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
	
	# # # presentation.xml
	def presentation(self, element, action):
		pass
	
	# # # slidemaster%n.xml
	def sldMaster(self, element, action):
		if action == "start":
			self.sm_flag = True #flag used to turn on/off the detection of placeholder tag
		else:
			self.sm_flag = False
	
	# # # slide%n.xml
	def sld(self, element, action):
		pass
	
	# # # chart%n.xml
	def chartSpace(self, element, action):
		#charts and drawings are not yet inserted in the middle of the slide content
		pass
	
	# # # notesMaster%n.xml
	def notesMaster(self, element, action):
		if action == "start":
			self.sm_flag = True #flag used to turn on/off the detection of placeholder tag
		else:
			self.sm_flag = False

	# # # notesSlide%n.xml
	def notes(self, element, action): #there are names to extract?
		#problem with notes, as their number may not start at 1
		pass

	# # # standard slide content
	def cSld(self, element, action):
		pass
	
	def spTree(self, element, action):
		pass

	def graphicFrame(self, element, action):
		pass

	def sp(self, element, action): #shape / textbox
		if action == "start" and self.sm_flag: #if during Slide Master parsing
			for ph in element.iterfind(".//{*}ph"):
				self.ph_flag = True
				break
		else:
			self.ph_flag = False

	def nvSpPr(self, element, action): #non-visual shape props
		pass

	def cNvPr(self, element, action):
		pass #there's a name attribute here
	
	def txBody(self, element, action):
		pass

	# # # standard paragraph content
	def p(self, element, action):
		if action == "start":
			return {"type": "paragraph", "content": "<p>", "track": True}
		else:
			return {"type": "paragraph", "content": "</p>", "track": True}
		
	def pPr(self, element, action):
		return {"type": None, "content": None, "track": False}
	
	def pStyle(self, element, action):
		#extract paragraph style
		return {"type": None, "content": None, "track": False}
	
	def r(self, element, action):
		return {"type": None, "content": None, "track": False}
	
	def rPr(self, element, action):
		return {"type": None, "content": None, "track": False}
		
	def t(self, element, action):
		if action == "start" and not self.ph_flag:
			content = ""
			if element.text != None:
				content = element.text
			return {"type": "text", "content": content, "track": False}

	def pt(self, element, action):
		if action == "start":
			return {"type": "paragraph", "content": "<p>", "track": True}
		else:
			return {"type": "paragraph", "content": "</p>", "track": True}
	
	def v(self, element, action):
		content = ""
		if action == "start":
			if element.text != None:
				content = element.text
			return {"type": "text", "content": content, "track": False}
