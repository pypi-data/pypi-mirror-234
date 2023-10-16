"""
OOXMILKER, an Office Open XML parser that outputs HTML.

Copyright 2021-2023 Hervé Leleu

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

import os
import sys
import shutil
import zipfile
import re
import xml.etree.ElementTree as ET
import importlib

# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# STANDALONE FUNCTIONS
# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

def read(document_path):
	"""
	Returns a generator. Each iteration gives a new paragraph.
	Usage: 
	input: string representing the path to an OOXML file
	output: iterable tuple
	"""
	oo_document = ooxml_document(document_path)
	
	if oo_document.open_document() != True:
		print (f"problem opening {document_path}")
		sys.exit(1)

	oo_handler = file_handler(oo_document.file_type, oo_document.files_list, oo_document.temp_dir)
	
	for text in oo_handler.parse_xml():
		yield text

	if oo_document.close_document() != True:
		print ("problem closing")
		sys.exit(1)


# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# CLASSES
# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

class ooxml_document:
	"""
	Management of the OOXML file: opening, listing out XML components and closing.
	"""
	def __init__(self, file_path):
		#instance variables
		self.file_name = os.path.basename(file_path)
		self.file_dir = os.path.abspath(file_path)[:-len(self.file_name)]
		self.temp_dir = os.path.join(self.file_dir, 'temp')
		self.files_list = []
		self.file_type = ''
		self.file_type_regex = ''
		#hardcoded data for finding file type (self.type_dict) and sorting xml files (self.sort_dict)
		self.type_dict = {'xl': 'xl(/|\\\\)workbook\\.xml', 'ppt': 'ppt(/|\\\\)presentation\\.xml', 'word': 'word(/|\\\\)document\\.xml', 'visio': 'visio(/|\\\\)document\\.xml'}
		self.sort_dict = {'xl': ['workbook.', 'sharedStrings.', 'sheet%n.', 'drawing%n.'], 'ppt': ['presentation.', 'slideMaster%n.', 'slide%n.', 'chart%n.', 'drawing%n.', 'notesMaster%n.', 'notesSlide%n.'], 'word': ['header%n.', 'footer%n.', 'document.', 'footnotes.', 'endnotes.'], 'visio': ['masters.', 'master%n.', 'pages.', 'page%n.']}

	def open_document(self):
		"""
		Checks OOXML file's accessibility, defines its file type (self.file_type), creates a list of prospective XML files for parsing and unpacks them in a temporary folder.
		output: boolean (True = success; False or None = failure)
		"""
		#checking file
		if os.path.isfile(os.path.join(self.file_dir, self.file_name)) != True:
			return False
		
		#getting file type and list of files
		with zipfile.ZipFile(os.path.join(self.file_dir, self.file_name), 'r') as zip_target:
			#detect filetype from files
			self.file_type = self._get_file_type(zip_target.namelist())
			if self.file_type == None:
				return False

			#getting a sorted list of files
			self.files_list = self._get_file_list(zip_target.namelist())

		#unzipping physical file
		with zipfile.ZipFile(os.path.join(self.file_dir, self.file_name), 'r') as zip_target:
			for file in self.files_list:
				zip_target.extract(file, self.temp_dir)
		
		return True
	
	def _get_file_type(self, list):
		file_type = None #default type
		files_string = ''.join(list)
		
		for k in self.type_dict:
			if re.search(self.type_dict[k], files_string) != None:
				file_type = k
				break

		return file_type

	def _get_file_list(self, files_list):
		sorted_list = []

		#main loop
		for p in self.sort_dict[self.file_type]:
			if "%n" in p:
				n = 0
				g = len(sorted_list)
				while len(sorted_list) >= g + n:
					n += 1
					sorted_list += (f for f in files_list if p.replace('%n',str(n)) in f)
			else:
				sorted_list += (f for f in files_list if p in f)
		
		#removing non-xml files such as '.rels'
		sorted_list[:] = (f for f in sorted_list if f[-4:] == '.xml')

		return sorted_list

	def close_document(self):
		"""
		Deletes temporary folder.
		output: boolean (True = success; False = failure)
		"""
		try:
			shutil.rmtree(self.temp_dir, ignore_errors=False, onerror=None)
		except:
			return False
		
		return True


class file_handler:
	"""
	Manages the series of XML files: parser module loading, contents parsing.
	"""
	def __init__(self, document_type, files_list, temp_folder, **kwargs):
		self.document_type = document_type
		
		#assigning the correct parser module based on document type
		if self.document_type == "word":
			self.ooxml_module = importlib.import_module(".docx_module", "ooxmilker.formats")
		elif self.document_type == "xl":
			self.ooxml_module = importlib.import_module(".xlsx_module", "ooxmilker.formats")
		elif self.document_type == "ppt":
			self.ooxml_module = importlib.import_module(".pptx_module", "ooxmilker.formats")
		elif self.document_type == "visio":
			self.ooxml_module = importlib.import_module(".vsdx_module", "ooxmilker.formats")
		else:
			pass
		
		#adding the full path to each prospective XML file
		self.files_list = []
		for f in files_list:
			self.files_list.append(os.path.join(temp_folder, f))
		
	def parse_xml(self):
		"""
		Iterates through XML files, parse contents, stores in buffer and releases tuples.
		output: tuple where [0] = text with HTML tags; [1] = flags (boolean)
		"""
		oop = getattr(self.ooxml_module, "xml_parser")() # <- instanciate xml_parser class from module loaded dynamically in __init__. Mind the () at the end.
		for xml_file in self.files_list:
			oob = buffer() #a new buffer is instanciated for each xml file 

			xml_context = ET.iterparse(xml_file, events=("start", "end"))
			for action, element in xml_context:
				#getting rid of tag's namespace
				tag = re.sub('\{.*?\}', '', element.tag)
				#changing "del" to "del_tag" because del is a keyword in Python
				if tag == "del":
					tag = "del_tag"

				#getting the paragraph, if any
				parsed_paragraph = ""
				parsed_paragraph = oob.store(tag, action, oop.parse_xml(tag, element, action))
				#skipping to the next iteration if the paragraph has no content
				if parsed_paragraph == None:
					continue
				if parsed_paragraph[0] == None:
					continue

				yield(parsed_paragraph)

	
class buffer:
	"""
	Stores pieces of text until they form a paragraph or a cell.
	"""
	def __init__(self):
		self.buffer = []         #buffer for the content of the paragraph
		self.forced = ""
		self.ancestry = []       #list of all ancestors of the current tag, in order
		self.flag_change = False #indicate the paragraph has some insertion or deletion
		self.flag_section = False
		self.flag_table = False  #indicate parent table
	
	def store(self, tag, action, parsed_data):
		"""
		Sends text to buffer, sets various flags, tracks ancestry if needed and checks whether the buffer can be released.
		input: tag, action from XML parser, parsed data (dictionary)
		output: full paragraph or cell (only if complete)
		"""
		#table flag
		if parsed_data["type"] == "table":
			if action == "start":
				self.flag_table = True

		#change flag
		if parsed_data["type"] == "insertion":
			self.flag_change = True
		elif parsed_data["type"] == "deletion":
			self.flag_change = True

		#condition: if track ancestry required
		if parsed_data["track"]:
			self._track_ancestry(tag, action)
		
		#populating buffer
		if parsed_data["content"] != None:
			self.buffer.append(parsed_data["content"].lstrip("\n"))

		return self._release(tag, action)

	def _release(self, tag, action):
		"""
		Releases the buffer only if tag is closing and if there is no ancestor.
		"""
		if len(self.ancestry) == 0:
			parsed_paragraph = ("".join(map(str, self.buffer)), {'tbl': self.flag_table, 'chg': self.flag_change})
			self.buffer = []
			self.flag_change = False
			self.flag_section = False
			if len(parsed_paragraph[0]) > 0:
				return parsed_paragraph
			else:
				pass
	
	def _track_ancestry(self, tag, action):
		if action == "start":
			self.ancestry.append(tag)
		elif action == "end":
			try:
				self.ancestry.pop()
			except:
				pass


# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# MAIN
# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

def main():
	print("Please refer to the manual.")

if __name__ == '__main__':
	main()
