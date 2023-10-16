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
		self.shared_strings = []
		self.ss_flag = False
		self.ss_counter = 0
	
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
	
	# # # from workbook.xml
	def workbook(self, element, action):
		pass
	
	def sheets(self, element, action):
		pass
	
	def sheet(self, element, action): #name of each sheet
		if action == "start":
			name = element.attrib.get("name")
			return {"type": "sheetname", "content": f"<p>{name}</p>", "track": False}
		else:
			pass

	# # # sharedStrings.xml
	#content from shared strings goes in a list
	def sst(self, element, action):
		if action == "start":
			self.ss_flag = True
		else:
			self.ss_flag = False

	def si(self, element, action): #counting the number of si gives away the cross-ref
		if action == "end":
			self.ss_counter += 1

	# # # from sheet[n].xml
	def worksheet(self, element, action):
		pass

	def cols(self, element, action):
		pass

	def col(self, element, action): #sheet hidden or not
		if action == "start":
			if element.attrib.get("{http://www.w3.org/XML/1998/namespace}hidden") != None:
				print(f'hidden') #rework
		else:
			pass

	def sheetData(self, element, action):
		pass
	
	def row(self, element, action):
		pass

	def c(self, element, action): #cell
		if action == "start":
			if element.attrib.get("t", None) == "s":
				self.ss_flag = True
		else:
			self.ss_flag = False

	def v(self, element, action): #value of the cell
		if action == "start":
			if self.ss_flag:
				return {"type": "cell", "content": f"<p>{self.shared_strings[int(element.text)]}</p>", "track": False}
			

	def dataValidation(self, element, action): #messages associated to data validation
		pass

	def headerFooter(self, element, action):
		pass #see page 1638 for all codes
	def firstFooter(self, element, action):
		pass
	def firstHeader(self, element, action):
		pass
	def oddFooter(self, element, action):
		pass
	def oddHeader(self, element, action):
		pass
	def evenFooter(self, element, action):
		pass
	def evenHeader(self, element, action):
		pass
	def drawingHF(self, element, action):
		pass

	# # # drawing%n.xml
	def wsDr(self, element, action):
		pass

	def wsDr(self, element, action):
		pass

	def twoCellAnchor(self, element, action):
		pass

	def sp(self, element, action):
		pass

	def txBody(self, element, action):
		pass
	
	# # # paragraph, run and text
	def p(self, element, action):
		if action == "start":
			return {"type": "paragraph", "content": "<p>", "track": True}
		else:
			return {"type": "paragraph", "content": "</p>", "track": True}

	def r(self, element, action): #rich text run
		return {"type": None, "content": None, "track": False}
	
	def rPr(self, element, action):
		#style like text size, font, bold, etc.
		pass
	
	def rPh(self, element, action): #phonetic/furigana for Japanese
		pass

	def t(self, element, action): #text
		#has to change behavior based on whether content is from shared strings or not.
		if action == "start":
			content = ""
			if element.text != None:
				preserve = element.attrib.get("{http://www.w3.org/XML/1998/namespace}space", None)
				if preserve == "preserve":
					content = element.text
				else:
					content = element.text.strip()
			if self.ss_flag: #if True, content goes to a list, that will be used by <c> and <v>
				if len(self.shared_strings) == self.ss_counter: #if item is new
					self.shared_strings.insert(self.ss_counter, content)
				else: #if item exists
					self.shared_strings[self.ss_counter] += content
			else: #if False, content is returned normally
				return {"type": "text", "content": content, "track": False}

	# # # additional text stuff
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
