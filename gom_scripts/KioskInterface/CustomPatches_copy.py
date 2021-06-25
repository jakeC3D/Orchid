# -*- coding: utf-8 -*-
# Script: Custom Patches
#
# PLEASE NOTE that this file is part of the GOM Inspect Professional software
# You are not allowed to distribute this file to a third party without written notice.
#
# Copyright (c) 2016 GOM GmbH
# Author: GOM Software Development Team (M.V.)
# All rights reserved.

# GOM-Script-Version: 7.6
#
# ChangeLog:
# 2012-05-31: Initial Creation
# 2013-04-15: Results are now grouped into different folders based on template
# 2013-09-03: Changed import statements to use relative imports thus the Setupscript can import it
#             (custom configurations will be kept)
# 2014-05-16: Use project token to get the based template name
# 2015-04-23: Added template for table of additional project keywords

from Base.Misc import Globals, Utils, DefaultSettings, Messages
from Base import Workflow, Evaluate
import gom
import os
import re
import sys 
import Orchid_Globals
import configparser 
import shutil 

config = configparser.ConfigParser() 
config_path = os.path.join(gom.app.public_directory, 'Orchid_Kiosk_Settings.cfg') 
config.read(config_path)
Globals.DIALOGS.STARTDIALOG=gom.script.sys.create_user_defined_dialog (content='<dialog>' \
' <title>Start Kiosk</title>' \
' <style></style>' \
' <control id="Empty"/>' \
' <position>left</position>' \
' <embedding>embedded_in_kiosk</embedding>' \
' <sizemode></sizemode>' \
' <size height="333" width="263"/>' \
' <content rows="9" columns="2">' \
'  <widget type="label" columnspan="1" row="0" column="0" rowspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Part Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::string" columnspan="1" row="0" column="1" rowspan="1">' \
'   <name>part_num</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="1" column="0" rowspan="1">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>Operation Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::string" columnspan="1" row="1" column="1" rowspan="1">' \
'   <name>op_num</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="2" column="0" rowspan="1">' \
'   <name>label_2</name>' \
'   <tooltip></tooltip>' \
'   <text>Work Order Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::string" columnspan="1" row="2" column="1" rowspan="1">' \
'   <name>work_num</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="3" column="0" rowspan="1">' \
'   <name>label_3</name>' \
'   <tooltip></tooltip>' \
'   <text>Template:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="3" column="1" rowspan="1">' \
'   <name>tn</name>' \
'   <tooltip></tooltip>' \
'   <text>Not Found</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="4" column="0" rowspan="1">' \
'   <name>label_4</name>' \
'   <tooltip></tooltip>' \
'   <text>Status:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="4" column="1" rowspan="1">' \
'   <name>status</name>' \
'   <tooltip></tooltip>' \
'   <text>Invalid Part Number</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="2" row="5" column="0" rowspan="1">' \
'   <name>select_sn</name>' \
'   <tooltip></tooltip>' \
'   <text>Enter Serial Numbers</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="2" row="6" column="0" rowspan="1">' \
'   <name>change_selection</name>' \
'   <tooltip></tooltip>' \
'   <text>Change Selected Template</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="2" row="7" column="0" rowspan="1">' \
'   <name>start</name>' \
'   <tooltip></tooltip>' \
'   <text>Start</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="2" row="8" column="0" rowspan="1">' \
'   <name>exit</name>' \
'   <tooltip></tooltip>' \
'   <text>Exit</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>cancel</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
' </content>' \
'</dialog>')
 

class StartUpV8( Workflow.StartUpV8, metaclass = Utils.MetaClassPatch ):

	def __init__(self,logger): 
		Workflow.StartUpV8.original____init__(self,logger) 
		self.dialog = Globals.DIALOGS.STARTDIALOG 
		self.dialog.handler = self.dialog_event_handler
		self.serial_found = False 
		self.temp_found = False
		self.set_up_values = False 
		self.sn_dict = {}
		self.page_num = ''
		self.sn_tracker = -1
		self.keys = []
		self.ENTER_SN=gom.script.sys.create_user_defined_dialog (content='<dialog>' \
' <title>Enter Serial Numbers</title>' \
' <style></style>' \
' <control id="Empty"/>' \
' <position>center</position>' \
' <embedding></embedding>' \
' <sizemode>automatic</sizemode>' \
' <size width="415" height="285"/>' \
' <content columns="4" rows="7">' \
'  <widget column="0" columnspan="1" row="0" type="label" rowspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Array Position:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="1" columnspan="1" row="0" type="label" rowspan="1">' \
'   <name>curr_array</name>' \
'   <tooltip></tooltip>' \
'   <text>A1</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="2" columnspan="1" row="0" type="label" rowspan="1">' \
'   <name>label_3</name>' \
'   <tooltip></tooltip>' \
'   <text>Jump to array:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="3" columnspan="1" row="0" type="input::string" rowspan="1">' \
'   <name>jump</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget column="0" columnspan="1" row="1" type="label" rowspan="1">' \
'   <name>label_4</name>' \
'   <tooltip></tooltip>' \
'   <text>Serial Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="1" columnspan="1" row="1" type="input::string" rowspan="1">' \
'   <name>sn</name>' \
'   <tooltip></tooltip>' \
'   <value>0</value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget column="2" columnspan="2" row="1" type="spacer::horizontal" rowspan="1">' \
'   <name>spacer</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>0</maximum_size>' \
'  </widget>' \
'  <widget column="0" columnspan="4" row="2" type="input::checkbox" rowspan="1">' \
'   <name>export_pdf</name>' \
'   <tooltip></tooltip>' \
'   <value>true</value>' \
'   <title>Export PDF</title>' \
'  </widget>' \
'  <widget column="0" columnspan="4" row="3" type="input::checkbox" rowspan="1">' \
'   <name>export_csv</name>' \
'   <tooltip></tooltip>' \
'   <value>true</value>' \
'   <title>Export CSV</title>' \
'  </widget>' \
'  <widget column="0" columnspan="1" row="4" type="button::pushbutton" rowspan="1">' \
'   <name>prev</name>' \
'   <tooltip></tooltip>' \
'   <text>Prev</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>arrow_left</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="1" columnspan="2" row="4" type="spacer::horizontal" rowspan="1">' \
'   <name>spacer_1</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>-1</maximum_size>' \
'  </widget>' \
'  <widget column="3" columnspan="1" row="4" type="button::pushbutton" rowspan="1">' \
'   <name>next</name>' \
'   <tooltip></tooltip>' \
'   <text>Next</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>arrow_right</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="0" columnspan="4" row="5" type="button::pushbutton" rowspan="1">' \
'   <name>back_to_start</name>' \
'   <tooltip></tooltip>' \
'   <text>Close</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="0" columnspan="4" row="6" type="button::pushbutton" rowspan="1">' \
'   <name>exit</name>' \
'   <tooltip></tooltip>' \
'   <text>Exit Kiosk</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>cancel</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
' </content>' \
'</dialog>')
		self.ENTER_SN.handler = self.sn_event_handler

	def open_template( self,  startup = False ):
		'''
		create a project from template
		if startup is given directly opens last used template
		''' 
		if not startup:
			# if the filter is unique (only one template would match)
			# directly open the project template
			unique_template = self.is_template_filter_unique()
			if unique_template is not None and unique_template == Globals.SETTINGS.CurrentTemplate:
				self.log.debug( 'already open' )
				self._after_template_opened( opened_template = {'template_name':unique_template} )
				return
			elif unique_template is not None:
				gom.script.sys.close_project ()
				template = gom.script.sys.create_project_from_template ( 
					config_level = Globals.SETTINGS.TemplateConfigLevel,
					template_name = unique_template )
				self.log.debug( 'opened automatically {}'.format( unique_template ) )
				template['template_name'] = unique_template
				self._after_template_opened( template )
				return
			elif Globals.SETTINGS.Inline:
				opened_template = {'template_name':None}
				self._after_template_opened( opened_template )
				return

		gom.script.sys.close_project ()
		opened_template = {'template_name':None}
		try:
			# called directly after dialog show
			if startup:
				template = gom.script.sys.create_project_from_template ( 
					config_level = Globals.SETTINGS.TemplateConfigLevel,
					template_name = Globals.SETTINGS.CurrentTemplate )
				opened_template['template_name'] = Globals.SETTINGS.CurrentTemplate
			# show the template dialog
			elif Globals.SETTINGS.ShowTemplateDialog:
				filter = self.Template_filter  # first get the filter before deactivating the dialog
				self.dialog.enabled = False
				opened_template=gom.script.sys.create_project_from_template (
					config_levels=[Globals.SETTINGS.TemplateConfigLevel], 
					template_name=Globals.SETTINGS.TemplateName, 
					regex_filters=filter)
			# dont show the template dialog
			else:
				template = gom.script.sys.create_project_from_template ( 
					config_level = Globals.SETTINGS.TemplateConfigLevel,
					template_name = Globals.SETTINGS.TemplateName )
				opened_template['template_name'] = Globals.SETTINGS.TemplateName
		except Globals.EXIT_EXCEPTIONS:
			raise
		except Exception as error:
			self.log.exception( str( error ) )
		finally:
			self.dialog.enabled = True

		self._after_template_opened( opened_template )
		self.log.info( 'opened template "{}"'.format( Globals.SETTINGS.CurrentTemplate ) )
		
	def load_programs(self): 
		self.programs_dict = {} 
		for sec in config.sections(): 
			if 'PROGRAM' in sec.upper(): 
				for (key, value) in config.items(sec): 
					print(key.upper().strip())
					if 'PART NUMBER' in key.upper().strip(): 
						pn = value 
					elif 'OPERATION NUMBER' in key.upper().strip(): 
						on = value 
					elif  'SCANNING TEMPLATE' in key.upper().strip():
						temp = value.split(',')
						st = []
						for i in temp: 
							st.append(i.strip()) 
					elif  'INSPECTION TEMPLATE' in key.upper().strip():
						temp = value.split(',')
						inspec_t = []
						for i in temp: 
							inspec_t.append(i.strip()) 
					elif 'PDF' in key.upper().strip(): 
						pdf = value 
					elif 'CSV' in key.upper().strip(): 
						csv = value 
					elif 'POSITION' in key.upper().strip(): 
						temp = value.split(',') 
						ap = [] 
						for i in temp: 
							ap.append(i.strip()) 
					elif key.upper().strip() == 'ARRAY': 
						a = value.strip()
					elif 'POLY' in key.upper().strip(): 
						poly = value.strip() 
				try:
					key = '{}_{}'.format(pn,on) 
					multiple = False 

					self.programs_dict['multiple'] = multiple
					self.programs_dict[key] = {'scanning_template':st, 'array' : a, 'poly' : poly.upper(), 'inspection_template': inspec_t, 'pdf' : pdf, 'csv' : csv, 'array_positions' : ap} 
				except Exception as err:
					print('Config is not complete:',err) 


	def search_for_template(self, select_again = False): 
		DIALOG=gom.script.sys.create_user_defined_dialog (content='<dialog>' \
' <title>Template Selection</title>' \
' <style></style>' \
' <control id="Close"/>' \
' <position></position>' \
' <embedding></embedding>' \
' <sizemode></sizemode>' \
' <size height="147" width="286"/>' \
' <content rows="2" columns="2">' \
'  <widget type="label" columnspan="1" row="0" column="0" rowspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Scanning Template:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::list" columnspan="1" row="0" column="1" rowspan="1">' \
'   <name>scan</name>' \
'   <tooltip></tooltip>' \
'   <items/>' \
'   <default></default>' \
'  </widget>' \
'  <widget type="label" columnspan="1" row="1" column="0" rowspan="1">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>Inspection Template:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::list" columnspan="1" row="1" column="1" rowspan="1">' \
'   <name>inspec</name>' \
'   <tooltip></tooltip>' \
'   <items/>' \
'   <default></default>' \
'  </widget>' \
' </content>' \
'</dialog>')
		project_names = [] 
		search_name = '{}_{}'.format(self.dialog.part_num.value.strip(),self.dialog.op_num.value)
		if search_name in self.programs_dict.keys(): 
			st = self.programs_dict[search_name]['scanning_template']
			inspec_t = self.programs_dict[search_name]['inspection_template'] 
			multiple = False
			if select_again or not 'selected_st' in self.programs_dict.keys(): 
				if len(st) == 1:
					st = st[0] 
				else: 
					multiple = True
					DIALOG.scan.items = st
					DIALOG.label_1.visible = False 
					DIALOG.inspec.visible = False
					gom.script.sys.show_user_defined_dialog(dialog = DIALOG) 
					st = DIALOG.scan.value 
				if len(inspec_t) == 1: 
					inspec_t = inspec_t[0] 
				else: 
					multiple = True 
					DIALOG.inspec.items = inspec_t
					DIALOG.label.visible = False 
					DIALOG.scan.visible = False
					DIALOG.label_1.visible = True 
					DIALOG.inspec.visible = True
					gom.script.sys.show_user_defined_dialog(dialog = DIALOG) 
					inspec_t = DIALOG.inspec.value 
				self.programs_dict['multiple'] = multiple
				self.programs_dict['selected_st'] = st 
				self.programs_dict['selected_it'] = inspec_t 
			elif 'selected_st' in self.programs_dict.keys(): 
				st = self.programs_dict['selected_st'] 
				inspec_t  =self.programs_dict['selected_it'] 
			if self.programs_dict['multiple']:
				self.dialog.change_selection.visible = True
			else:
				self.dialog.change_selection.visible = False 
			self.project_path = os.path.join(config['Template Locations']['scanning'], st + '.project_template') 
			print(self.project_path) 
			inspec_template = os.path.join(config['Template Locations']['inspection'],inspec_t + '.project_template') 
			print(inspec_template) 
			if os.path.exists(self.project_path):
				print('Scanning template found')
				if not os.path.exists(inspec_template): 
					self.temp_found = False 
					self.dialog.tn.text = 'Inspection Template Not Found'
				else:
					print('Inspection Template Found')
					self.temp_found = True 
					self.programs_dict['selected_st'] = st 
					self.programs_dict['selected_it'] = inspec_t 
					print('ST:',st) 
					self.dialog.tn.text = st
					print('Update text')
			else: 
				self.temp_found = False 
				self.dialog.tn.text = 'Scanning Template Not Found'
	
	def move_template(self, t_name): 
		self.new_path = os.path.join(gom.app.public_directory,'gom_project_templates', t_name + '.project_template') 
		old_path = os.path.join(config['Template Locations']['scanning'], t_name + '.project_template') 
		shutil.copy(old_path,self.new_path) 
		
	def remove_template(self): 
		os.remove(self.new_path) 
		
	def enable_continue(self): 
		if self.dialog.part_num.value != '' and self.dialog.op_num.value != '' and self.dialog.work_num.value != '' and self.temp_found: 
			self.dialog.select_sn.enabled = True 
			if self.serial_found:
				self.dialog.start.enabled = True 
		else:
			self.dialog.select_sn.enabled = False 
			self.dialog.start.enabled = False 

	def update_status(self): 
		if self.dialog.part_num.value == '': 
			self.dialog.status.text = 'Enter Part Number' 
		elif self.dialog.op_num.value == '':
			self.dialog.status.text = 'Enter Operation Number' 
		elif self.dialog.work_num.value == '':
			self.dialog.status.text = 'Enter Work Number' 
		elif not self.temp_found: 
			self.dialog.status.text = 'No template selected' 
		elif not self.serial_found:
			self.dialog.status.text = 'Please enter serial number(s)' 
		else:
			self.dialog.status.text = 'Ready' 
			self.dialog.start.enabled = True 
	
	def reset_dicts(self): 
		self.serial_found = False 
		self.temp_found = False
		self.set_up_values = False 
		self.sn_dict = {}
		self.page_num = ''
	
	def dialog_event_handler (self,widget):
		if isinstance(widget,str): 
			if widget == 'initialize': 
				self.load_programs()
				if self.programs_dict['multiple']: 
					self.dialog.change_selection.visible = True 
				else:
					self.dialog.change_selection.visible = False 
				self.dialog.select_sn.enabled = False 
				self.dialog.start.enabled = True 
				self.dialog.part_num.value = '' 
				self.dialog.op_num.value = '' 
				self.dialog.work_num.value = '' 
				self.reset_dicts()
		elif widget.name == 'change_selection':
			self.search_for_template(True) 
		elif widget.name == 'select_sn':
			self.search_name = '{}_{}'.format(self.dialog.part_num.value.strip(),self.dialog.op_num.value) 
			enter_sn_result=gom.script.sys.show_user_defined_dialog (dialog=self.ENTER_SN)
			#Open serial selection 
		elif widget.name == 'start':
			self.move_template(self.dialog.tn.text)
			Globals.SETTINGS.CurrentTemplate = self.dialog.tn.text
			self.open_template()
			self.remove_template()
			gom.script.sys.close_user_defined_dialog(dialog = self.dialog, result = True) 
		elif widget.name == 'exit': 
			gom.script.sys.close_user_defined_dialog(dialog = self.dialog, result = False) 
			sys.exit(0)
		self.search_for_template()
		print('Seared for template')
		self.update_status()
		print('Updated Status')
		self.enable_continue() 
		print('Tried to enable continue') 

	def array_dict(self): 
		array_list = self.programs_dict[self.search_name]['array_positions'] #Returns list of array positions  
		array_positions = []
		for a in array_list: 
			print(a)
			temp_range = re.findall(r'\d+',a) 
			letter = re.match(r'\w',a)[0] 
			first = int(temp_range[0]) 
			second = int(temp_range[-1]) + 1
			for i in range(first,second): 
				temp_var = '{}{}'.format(letter,i) 
				array_positions.append(temp_var)
		return array_positions
 

	def set_up(self):
		print('Setting up...') 
		self.keys = self.array_dict()
		self.set_up_values = True 
		self.ENTER_SN.prev.enabled = False 
		alpha_index = 0 
		alpha_list = ['A','B','C','D','E']
		num = 1 
		for key in self.keys: 
			if self.page_num == '': 
				self.page_num = key 
				print('Initial value of page number:',self.page_num)
			value = [0,True,True]  
			self.sn_dict[key] = value 
		print('sn dict:',self.sn_dict) 
		print('self.keys:',self.keys) 
		
	def update_page(self,jump_to = None):
		if jump_to and jump_to in self.sn_dict.keys(): 
			print('Updating page_num') 
			self.page_num = jump_to  
			self.ENTER_SN.sn.enabled = True 
			self.ENTER_SN.export_csv.enabled = True
			self.ENTER_SN.export_pdf.enabled = True 
		elif jump_to and not jump_to in self.sn_dict.keys(): 
			self.ENTER_SN.curr_array.text = 'Invalid array value'
			self.ENTER_SN.sn.enabled = False 
			self.ENTER_SN.export_csv.enabled = False 
			self.ENTER_SN.export_pdf.enabled = False 
		elif jump_to == '':
			self.ENTER_SN.sn.enabled = True 
			self.ENTER_SN.export_csv.enabled = True
			self.ENTER_SN.export_pdf.enabled = True
		self.ENTER_SN.curr_array.text = self.page_num
		self.ENTER_SN.sn.value = self.sn_dict[self.page_num][0] 
		self.ENTER_SN.export_csv.value = self.sn_dict[self.page_num][1] 
		self.ENTER_SN.export_pdf.value = self.sn_dict[self.page_num][2] 
		
	def update_dict(self): 
		print(self.page_num) 
		print(self.sn_dict[self.page_num]) 
		self.sn_dict[self.page_num][0] = self.ENTER_SN.sn.value 
		self.sn_dict[self.page_num][1] = self.ENTER_SN.export_csv.value 
		self.sn_dict[self.page_num][2] = self.ENTER_SN.export_pdf.value
		
	def check_buttons(self): 
		if self.page_num == self.keys[-1]:
			self.ENTER_SN.next.enabled = False 
		else:
			self.ENTER_SN.next.enabled = True
		if self.page_num == self.keys[0]:
			self.ENTER_SN.prev.enabled = False 
		else:
			self.ENTER_SN.prev.enabled = True 
		
	def next_page(self): 
		self.ENTER_SN.jump.value = '' 
		curr_index = self.keys.index(self.page_num) 
		curr_index += 1 
		self.page_num = self.keys[curr_index] 
		if self.page_num == self.keys[-1]:
			self.ENTER_SN.next.enabled = False 
		else:
			self.ENTER_SN.next.enabled = True 
		
	def prev_page(self): 
		self.ENTER_SN.jump.value = '' 
		curr_index = self.keys.index(self.page_num) 
		curr_index -= 1 
		self.page_num = self.keys[curr_index] 
		if self.page_num == self.keys[0]:
			self.ENTER_SN.prev.enabled = False 
		else:
			self.ENTER_SN.prev.enabled = True 
			
	def check_for_serial(self):
		self.serial_found = False 
		for key in self.sn_dict: 
			if not self.sn_dict[key][0] in [0,'0'] : 
				self.serial_found = True 
			else:
				Orchid_Globals.skip_list.append(key)
			
	
	def sn_event_handler (self,widget):
		if isinstance(widget,str): 
			if widget == 'initialize': 
				self.ENTER_SN.sn.focus = True
				self.ENTER_SN.timer.enabled = True 
				self.ENTER_SN.timer.interval = 100
				if not self.set_up_values:
					self.set_up() 
		elif widget.name == 'next': 
			self.ENTER_SN.sn.focus = True
			self.next_page() 
			self.update_page() 
		elif widget.name == 'prev': 
			self.prev_page() 
			self.update_page() 
		elif widget.name in ['sn','export_csv','export_pdf']: 
			self.update_dict()
		elif widget.name == 'jump': 
			try:
				self.update_page(self.ENTER_SN.jump.value.upper()) 
				print(self.ENTER_SN.jump.value.upper())
			except Exception as err:
				print('Invalid value:',err) 
		elif widget.name == 'back_to_start': 
			self.check_for_serial() 
			gom.script.sys.close_user_defined_dialog(dialog = self.ENTER_SN) 
		elif widget.name == 'exit': 
			gom.script.sys.close_user_defined_dialog(dialog = self.dialog)
			gom.script.sys.close_user_defined_dialog(dialog = self.ENTER_SN) 
			sys.exit(0) 
		self.check_buttons()
		if self.ENTER_SN.export_pdf.focus or self.ENTER_SN.export_csv.focus: 
			self.ENTER_SN.next.focus = True 
		
class PatchedEvaluationAnalysis( Evaluate.EvaluationAnalysis, metaclass = Utils.MetaClassPatch ):
	@staticmethod
	def export_results( result ):
		'''
		This function is called directly after the Approve/Disapprove button is clicked in the confirmation dialog or after async evaluation. It stores the
		current project to a directory. You may want to patch this function for example to export measurement
		information to your needs.

		Arguments:
		result - True if user approved measurement data, otherwise False
		'''
		# call of the original function to export ginspect and pdf
		Evaluate.EvaluationAnalysis.original__export_results( result )

		( project_name, export_path ) = Evaluate.Evaluate.export_path_info()
		if not os.path.exists( export_path ):
			os.makedirs( export_path )

		# if the original export_results function was called the failed postfix is already part of the current project name
		# if not result:  # append failed postfix on failure
		# 	project_name += Globals.SETTINGS.FailedPostfix

		# Activate the following line if your custom exports below need to be executed in the result alignment.
		# Alternatively, you can also pass a specific alignment (name) as parameter.
		#Evaluate.EvaluationAnalysis.switch_to_result_alignment()

		# Start recording the custom export here
		# use for your export function as file parameter e.g.
		# file = os.path.join(export_path,project_name+'.txt'),

if __name__ == '__main__':
	Workflow.start_workflow()





