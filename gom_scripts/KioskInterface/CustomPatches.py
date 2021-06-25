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
# C3D Custom Kiosk 
#
# Author: C3D Scripting Team 
# Version: 1.2.1 
#
# Change Log (YYYY-MM-DD): 
# 2019-11-27: v1.0.0 - Initial Creation 
# 2020-5-12:  v1.1.1 - Added Overview table and fixed Part name bug 
# Version 1.2.1 (2020-12-11): Checking all inspection for out of tolerance and updating failed keyword

from Base.Misc import Globals, Utils, DefaultSettings, Messages
from Base.Communication import AsyncClient
from Base import Workflow, Evaluate
import gom
import os
import re
import sys 
import configparser 
import shutil 
import time 

VERSION = '1.2.1'

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
' <size height="430" width="326"/>' \
' <content columns="4" rows="11">' \
'  <widget type="label" columnspan="1" rowspan="1" column="0" row="0">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Part Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::string" columnspan="3" rowspan="1" column="1" row="0">' \
'   <name>part_num</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget type="label" columnspan="1" rowspan="1" column="0" row="1">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>Operation Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::string" columnspan="3" rowspan="1" column="1" row="1">' \
'   <name>op_num</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget type="label" columnspan="1" rowspan="1" column="0" row="2">' \
'   <name>label_2</name>' \
'   <tooltip></tooltip>' \
'   <text>Work Order Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::string" columnspan="3" rowspan="1" column="1" row="2">' \
'   <name>work_num</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget type="label" columnspan="1" rowspan="1" column="0" row="3">' \
'   <name>label_3</name>' \
'   <tooltip></tooltip>' \
'   <text>Template:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="label" columnspan="3" rowspan="1" column="1" row="3">' \
'   <name>tn</name>' \
'   <tooltip></tooltip>' \
'   <text>Not Found</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="label" columnspan="1" rowspan="1" column="0" row="4">' \
'   <name>label_4</name>' \
'   <tooltip></tooltip>' \
'   <text>Status:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="label" columnspan="3" rowspan="1" column="1" row="4">' \
'   <name>status</name>' \
'   <tooltip></tooltip>' \
'   <text>Invalid Part Number</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="4" rowspan="1" column="0" row="5">' \
'   <name>select_sn</name>' \
'   <tooltip></tooltip>' \
'   <text>Enter Serial Numbers</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="4" rowspan="1" column="0" row="6">' \
'   <name>overview</name>' \
'   <tooltip></tooltip>' \
'   <text>Overview Table</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="4" rowspan="1" column="0" row="7">' \
'   <name>change_selection</name>' \
'   <tooltip></tooltip>' \
'   <text>Change Selected Template</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="4" rowspan="1" column="0" row="8">' \
'   <name>start</name>' \
'   <tooltip></tooltip>' \
'   <text>Start</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="button::pushbutton" columnspan="4" rowspan="1" column="0" row="9">' \
'   <name>exit</name>' \
'   <tooltip></tooltip>' \
'   <text>Exit</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>cancel</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget type="spacer::horizontal" columnspan="2" rowspan="1" column="0" row="10">' \
'   <name>spacer</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>-1</maximum_size>' \
'  </widget>' \
'  <widget type="spacer::horizontal" columnspan="1" rowspan="1" column="2" row="10">' \
'   <name>spacer_1</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>-1</maximum_size>' \
'  </widget>' \
'  <widget type="label" columnspan="1" rowspan="1" column="3" row="10">' \
'   <name>version_number</name>' \
'   <tooltip></tooltip>' \
'   <text>0.0.0</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
' </content>' \
'</dialog>')
 
class StartUpV8( Workflow.StartUpV8, metaclass = Utils.MetaClassPatch ):

	def __init__(self,logger): 
		Workflow.StartUpV8.original____init__(self,logger) 
		self.dialog = Globals.DIALOGS.STARTDIALOG 
		self.dialog.handler = self.dialog_event_handler
		self.dialog.version_number.text = VERSION
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
' <size width="469" height="355"/>' \
' <content rows="9" columns="4">' \
'  <widget column="0" row="0" columnspan="1" type="label" rowspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Array Position:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="1" row="0" columnspan="1" type="label" rowspan="1">' \
'   <name>curr_array</name>' \
'   <tooltip></tooltip>' \
'   <text>A1</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="2" row="0" columnspan="1" type="label" rowspan="1">' \
'   <name>label_3</name>' \
'   <tooltip></tooltip>' \
'   <text>Jump to array:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="3" row="0" columnspan="1" type="input::string" rowspan="1">' \
'   <name>jump</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget column="0" row="1" columnspan="1" type="label" rowspan="1">' \
'   <name>label_4</name>' \
'   <tooltip></tooltip>' \
'   <text>Serial Number:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="1" row="1" columnspan="1" type="input::string" rowspan="1">' \
'   <name>sn</name>' \
'   <tooltip></tooltip>' \
'   <value></value>' \
'   <read_only>false</read_only>' \
'  </widget>' \
'  <widget column="2" row="1" columnspan="1" type="spacer::horizontal" rowspan="2">' \
'   <name>spacer_2</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>-1</maximum_size>' \
'  </widget>' \
'  <widget column="3" row="1" columnspan="1" type="button::pushbutton" rowspan="1">' \
'   <name>autofill</name>' \
'   <tooltip></tooltip>' \
'   <text>Autofill</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="0" row="2" columnspan="2" type="spacer::vertical" rowspan="2">' \
'   <name>spacer_4</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>2</maximum_size>' \
'  </widget>' \
'  <widget column="3" row="2" columnspan="1" type="button::pushbutton" rowspan="1">' \
'   <name>clear_all</name>' \
'   <tooltip></tooltip>' \
'   <text>Reset SNs</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="2" row="3" columnspan="2" type="spacer::horizontal" rowspan="1">' \
'   <name>spacer</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>0</maximum_size>' \
'  </widget>' \
'  <widget column="0" row="4" columnspan="4" type="input::checkbox" rowspan="1">' \
'   <name>export_pdf</name>' \
'   <tooltip></tooltip>' \
'   <value>true</value>' \
'   <title>Export PDF</title>' \
'  </widget>' \
'  <widget column="0" row="5" columnspan="4" type="input::checkbox" rowspan="1">' \
'   <name>export_csv</name>' \
'   <tooltip></tooltip>' \
'   <value>true</value>' \
'   <title>Export CSV</title>' \
'  </widget>' \
'  <widget column="0" row="6" columnspan="1" type="button::pushbutton" rowspan="1">' \
'   <name>prev</name>' \
'   <tooltip></tooltip>' \
'   <text>Prev</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>arrow_left</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="1" row="6" columnspan="2" type="spacer::horizontal" rowspan="1">' \
'   <name>spacer_1</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>-1</maximum_size>' \
'  </widget>' \
'  <widget column="3" row="6" columnspan="1" type="button::pushbutton" rowspan="1">' \
'   <name>next</name>' \
'   <tooltip></tooltip>' \
'   <text>Next</text>' \
'   <type>push</type>' \
'   <icon_type>system</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>arrow_right</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="0" row="7" columnspan="4" type="button::pushbutton" rowspan="1">' \
'   <name>back_to_start</name>' \
'   <tooltip></tooltip>' \
'   <text>Close</text>' \
'   <type>push</type>' \
'   <icon_type>none</icon_type>' \
'   <icon_size>icon</icon_size>' \
'   <icon_system_type>ok</icon_system_type>' \
'   <icon_system_size>default</icon_system_size>' \
'  </widget>' \
'  <widget column="0" row="8" columnspan="4" type="button::pushbutton" rowspan="1">' \
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
		self.REVIEW=gom.script.sys.create_user_defined_dialog (content='<dialog>' \
' <title>Review</title>' \
' <style></style>' \
' <control id="Close"/>' \
' <position>center</position>' \
' <embedding></embedding>' \
' <sizemode>fixed</sizemode>' \
' <size width="472" height="519"/>' \
' <content rows="2" columns="1">' \
'  <widget column="0" row="0" columnspan="1" type="display::log" rowspan="1">' \
'   <name>log</name>' \
'   <tooltip></tooltip>' \
'   <word_wrap>true</word_wrap>' \
'   <show_save>false</show_save>' \
'   <save_dialog_title>Save Log File</save_dialog_title>' \
'   <scroll_automatically>true</scroll_automatically>' \
'  </widget>' \
'  <widget column="0" row="1" columnspan="1" type="spacer::horizontal" rowspan="1">' \
'   <name>spacer</name>' \
'   <tooltip></tooltip>' \
'   <minimum_size>0</minimum_size>' \
'   <maximum_size>-1</maximum_size>' \
'  </widget>' \
' </content>' \
'</dialog>')
		self.REVIEW.handler = self.review_event_handler

	def open_template( self, project_to_open,startup = False, multipart = None ):
		'''
		create a project from template
		if startup is given directly opens last used template
		'''
		if not startup:
			# if the filter is unique (only one template would match)
			# directly open the project template
			unique_template, unique_cfg = self.is_template_filter_unique()
			if unique_template is not None and unique_template == Globals.SETTINGS.CurrentTemplate and Globals.SETTINGS.CurrentTemplateCfg == unique_cfg:
				self.log.debug( 'already open' )
				self._after_template_opened( opened_template = {'template_name':unique_template, 'config_level': unique_cfg} )
				return
			elif unique_template is not None:
				gom.script.sys.close_project ()
				if Globals.DRC_EXTENSION is not None and Globals.DRC_EXTENSION.PrimarySideActive():
					template = dict()
					template['template_name'] = unique_template
					template['config_level'] = unique_cfg
					template['DRC_Ext_DelayedLoading']=True
				else:
					template = gom.script.sys.create_project_from_template ( 
						config_level = unique_cfg,
						template_name = unique_template )
					self.log.debug( 'opened automatically {}'.format( unique_template ) )
					template['template_name'] = unique_template
					template['config_level'] = unique_cfg
				self._after_template_opened( template )
				return
			elif Globals.SETTINGS.Inline:
				opened_template = {'template_name':None, 'config_level':None}
				self._after_template_opened( opened_template )
				return

		gom.script.sys.close_project ()
		opened_template = {'template_name':None, 'config_level':None}
		try:
			cfg_level = [Globals.SETTINGS.TemplateConfigLevel]
			if cfg_level[0] == 'both':
				cfg_level = ['shared', 'user']
			# called directly after dialog show or for multipart
			if startup:
				template = gom.script.sys.create_project_from_template ( 
					config_level = Globals.SETTINGS.CurrentTemplateCfg,
					template_name = Globals.SETTINGS.CurrentTemplate )
				opened_template['template_name'] = Globals.SETTINGS.CurrentTemplate
				opened_template['config_level'] = Globals.SETTINGS.CurrentTemplateCfg
			# show the template dialog
			elif Globals.SETTINGS.ShowTemplateDialog:
				filter = self.Template_filter  # first get the filter before deactivating the dialog
				self.dialog.enabled = False
				if Globals.DRC_EXTENSION is not None and Globals.DRC_EXTENSION.PrimarySideActive():
					# open script later
					visible_templates = gom.interactive.sys.get_visible_project_templates ( 
						config_levels = cfg_level,
						regex_filters = filter )
					opened_template['template_name'] = visible_templates['template_name']
					opened_template['config_level'] = visible_templates['config_level']
					opened_template['DRC_Ext_DelayedLoading']=True
				else:
					opened_template = gom.interactive.sys.create_project_from_template ( 
						config_levels = cfg_level,
						template_name = Globals.SETTINGS.TemplateName,
						regex_filters = filter )
			# dont show the template dialog
			else:
				template = gom.script.sys.create_project_from_template ( 
					config_level = Globals.SETTINGS.TemplateConfigLevel,
					template_name = Globals.SETTINGS.TemplateName )
				opened_template['template_name'] = Globals.SETTINGS.TemplateName
				opened_template['config_level'] = Globals.SETTINGS.TemplateConfigLevel
		except Globals.EXIT_EXCEPTIONS:
			raise
		except Exception as error:
			self.log.exception( str( error ) )
		finally:
			self.dialog.enabled = True
		print('Log 100:',project_to_open) 
		gom.script.sys.load_project (
			file=project_to_open, 
			load_working_copy=False)
		res = self._after_template_opened( opened_template, multipart )
		self.log.info( 'opened template "{}"'.format( Globals.SETTINGS.CurrentTemplate ) )
		return res
		
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
					print(self.programs_dict)
				except Exception as err:
					print('Config is not complete:',err) 

	def increment_serial(self,t): 
		nums = re.findall('[0-9]+',t) 
		words = re.findall('[^\d]+',t) #Anything that is not a number  
	
		joined = ''.join(nums) 
		joined = int(joined) + 1
		joined = str(joined)
		new_serial = '' 
		nums.reverse() 
		words.reverse()
		new_serial = '' 
		for i in range(0,len(nums)):
			length = len(nums[i]) 
			new = (length) * -1  
			if not i: 
				if not words: 
					new_serial = '{}'.format(joined)
					return new_serial
				elif i + 1 <= len(words): 
					try:
						check = int(t[-1]) 
						words_first = False 
						new_serial = '{}{}'.format(words[i],joined[new:])
					except Exception as err:
						words_first = True 
						new_serial = '{}{}'.format(joined[new:],words[i])
				else:
					new_serial = '{}'.format(joined[new:])
				joined = joined[:new] 
				continue 
			if i +1 <= len(words):  
				if words_first:
					new_serial = '{}{}{}'.format(joined[new:],words[i],new_serial)
				else:
					new_serial = '{}{}{}'.format(words[i],joined[new:],new_serial)
			else:
				'{}{}'.format(joined[new:],new_serial)
			if i + 1 == len(nums): 
				new_serial = '{}{}'.format(joined,new_serial)
			joined = joined[:new]
		if i + 1 < len(words): 
			new_serial = '{}{}'.format(''.join(words[i+1:]),new_serial)
		
		return new_serial

	def autofill(self):
		new_serial = self.ENTER_SN.sn.value 
		for key in self.keys:
			self.sn_dict[key] = [new_serial,self.ENTER_SN.export_csv.value,self.ENTER_SN.export_pdf.value] 
			new_serial = self.increment_serial(new_serial)
		return True 
	
	def clear_all(self):
		self.ENTER_SN.sn.value = '' 
		self.ENTER_SN.export_pdf.value = True 
		self.ENTER_SN.export_csv.value = True 
		for key in self.keys:
			self.sn_dict[key] = ['',True,True] 
		return True
	
	def review_event_handler (self,widget):
		if widget == 'initialize': 
			output_string = 'Zone : Serial Number\n' 
			for key,value in self.sn_dict.items(): 
				f = '{} : {}\n\n'.format(key,value[0]) 
				output_string += f
			self.REVIEW.log.text = output_string 

	def search_for_template(self, select_again = False): 
		DIALOG=gom.script.sys.create_user_defined_dialog (content='<dialog>' \
' <title>Template Selection</title>' \
' <style></style>' \
' <control id="Close"/>' \
' <position>center</position>' \
' <embedding></embedding>' \
' <sizemode></sizemode>' \
' <size width="286" height="147"/>' \
' <content rows="2" columns="2">' \
'  <widget type="label" row="0" column="0" columnspan="1" rowspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Scanning Template:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::list" row="0" column="1" columnspan="1" rowspan="1">' \
'   <name>scan</name>' \
'   <tooltip></tooltip>' \
'   <items/>' \
'   <default></default>' \
'  </widget>' \
'  <widget type="label" row="1" column="0" columnspan="1" rowspan="1">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>Inspection Template:</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::list" row="1" column="1" columnspan="1" rowspan="1">' \
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
					self.programs_dict['selected_it_location'] = inspec_template
					print('ST:',st) 
					self.dialog.tn.text = st
					print('Update text')
			else: 
				self.temp_found = False 
				self.dialog.tn.text = 'Scanning Template Not Found'
		else:
			self.temp_found = False 
			self.dialog.tn.text = 'Not Found' 

	def move_template(self, t_name): 
		self.new_path = os.path.join(gom.app.public_directory,'gom_project_templates', 'Temp' + '.project_template') 
		old_path = os.path.join(config['Template Locations']['scanning'], t_name + '.project_template') 
		shutil.copy(old_path,self.new_path) 
		
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
		self.set_up_values = False 
	
	def dialog_event_handler (self,widget):
		if isinstance(widget,str): 
			if widget == 'initialize':
				self.temp_found = False 
				self.dialog.tn.text = 'Not Found'
				self.load_programs()
				self.update_status()
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
		elif widget.name == 'overview': 
			RESULT=gom.script.sys.show_user_defined_dialog (dialog=self.REVIEW)
		elif widget.name == 'start':
			self.move_template(self.dialog.tn.text)
			#Globals.SETTINGS.CurrentTemplate = self.dialog.tn.text
			Globals.SETTINGS.ShowTemplateDialog = False
			self.open_template(self.new_path )
		#	self.remove_template()
			gom.script.sys.close_user_defined_dialog(dialog = self.dialog, result = True) 
			self.set_project_keywords()
			self.delete_unwanted_points()
		elif widget.name == 'exit': 
			gom.script.sys.close_user_defined_dialog(dialog = self.dialog, result = False) 
			sys.exit(0)

		self.search_for_template(True)
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
			if not temp_range: 
				temp_var = letter
				array_positions.append(temp_var)
			else:
				first = int(temp_range[0]) 
				second = int(temp_range[-1]) + 1
				for i in range(first,second): 
					temp_var = '{}{}'.format(letter,i) 
					array_positions.append(temp_var)
		return array_positions
 
	def delete_unwanted_points(self): 
		for value in self.delete_list: 
			try:
				gom.script.cad.delete_element (
					elements=[gom.app.project.inspection[value]], 
					with_measuring_principle=True)
			except Exception as err:
				print(err) 


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
			value = ['',True,True]  
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
		
	def set_project_keywords(self): 
		print('Setting keywords...')
		try:
			gom.script.sys.set_project_keywords (
				keywords={'info_path': self.file_path}, 
				keywords_description={'info_path': 'Path for Inspection Instructions'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'info_name': self.filename}, 
				keywords_description={'info_name': 'File Name for Inspection Instructions'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'work_order': self.dialog.work_num.value}, 
				keywords_description={'work_order': 'Work Order Number'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'array_type': self.programs_dict[self.search_name]['array']}, 
				keywords_description={'array_type': 'Array Type (For Script)'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'poly_type': self.programs_dict[self.search_name]['poly']}, 
				keywords_description={'poly_type': 'Polygonize Type (For Script)'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'inspect_location': self.programs_dict['selected_it_location'] }, 
				keywords_description={'inspect_location': 'Inspection Template Location'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'csv_export_path': self.programs_dict[self.search_name]['csv'] }, 
				keywords_description={'csv_export_path': 'Export Path for CSV'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'pdf_export_path': self.programs_dict[self.search_name]['pdf'] }, 
				keywords_description={'pdf_export_path': 'Export Path for pdf'})
		except Exception as err:
			print(err) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'delete_location': self.new_path }, 
				keywords_description={'delete_location': 'Delete temp file'})
		except Exception as err:
			print(err) 
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
		output = '' 
		instruc_folder = os.path.join(gom.app.public_directory, 'inspection_instruction')  
		if not os.path.exists(instruc_folder): 
			os.makedirs(instruc_folder) 
		count = 1
		info_files = os.listdir(instruc_folder) 
		while True: 
			self.filename = 'info_{}.txt'.format(count) 
			if self.filename in info_files: 
				count += 1 
			else:
				self.file_path = os.path.join(instruc_folder, self.filename) 
				break 
		self.serial_found = False 
		self.delete_list = []
		for key in self.sn_dict: 
			if not self.sn_dict[key][0] in [0,'0', '']: 
				self.serial_found = True 
				sn = self.sn_dict[key][0]
				csv = self.sn_dict[key][1]
				pdf = self.sn_dict[key][2]
				formatted_string ='{}:{},{},{}\n'.format(key, sn, csv, pdf) 
				output += formatted_string 
			else:
				self.delete_list.append(key)
		with open(self.file_path, 'w') as my_file:
			my_file.write(output) 
		
	def sn_event_handler (self,widget):
		if isinstance(widget,str): 
			if widget == 'initialize': 
				self.ENTER_SN.sn.focus = True
				self.ENTER_SN.timer.enabled = True 
				self.ENTER_SN.timer.interval = 100
				if not self.set_up_values:
					self.set_up() 
					self.update_page()
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
		elif widget.name == 'autofill':
			self.autofill()
		elif widget.name == 'clear_all': 
			self.clear_all()
		if self.page_num == self.keys[0]:
			self.ENTER_SN.clear_all.visible = True 
			self.ENTER_SN.autofill.visible = True
		else:
			self.ENTER_SN.clear_all.visible = False
			self.ENTER_SN.autofill.visible = False 
		if self.ENTER_SN.sn.value != '': 
			self.ENTER_SN.autofill.enabled = True 
		else:
			self.ENTER_SN.autofill.enabled = False 
		self.check_buttons()
		if self.ENTER_SN.export_pdf.focus or self.ENTER_SN.export_csv.focus: 
			self.ENTER_SN.next.focus = True 
		
class PatchedEvaluationAnalysis( Evaluate.EvaluationAnalysis, metaclass = Utils.MetaClassPatch ):
	
	def get_poly_type(self, type): 
		if type.upper() == 'A':
			return 'detailed' 
		elif type.upper() == 'B': 
			return 'standard' 
		elif type.upper() == 'C': 
			return 'removes_surface_roughness'
		elif type.upper() == 'D': 
			return 'rough_inspection' 
		elif type.upper() == 'E': 
			return 'preview_meshes'
		else:
			return 'standard' 
			
	def polygonize( self ):
		'''
		polygonize measurement. The parameters for gom.script.atos.polygonize_and_recalculate get read from the setting file.

		Returns:
		returns the same as gom.script.atos.polygonize_and_recalculate of None if an exception occures.
		'''
		try:
			os.remove(gom.app.project.user_delete_location) 
		except Exception as err:
			print(err) 
		self.log.info( 'polygonize' )
		if self.parent.Dialog is not None:
			self.parent.Dialog.process_msg( step = self.parent.Dialog.Process_msg_step + 1 )
			self.parent.Dialog.process_msg_detail( Globals.LOCALIZATION.msg_evaluate_detail_msg_polygonize )
			self.parent.Dialog.processbar_step( 0 )
			self.parent.Dialog.processbar_max_steps( 3 )
		for ms in gom.app.project.measurement_series:
			print(ms.type)
			if ms.type == 'atos_measurement_series':
				ms_name = ms.name 
				break
		cube_height = config[gom.app.project.user_array_type]['height']
		cube_width = config[gom.app.project.user_array_type]['width']
		cube_length = config[gom.app.project.user_array_type]['length'] 
		poly_type = config['Poly Types'][gom.app.project.user_poly_type]
		poly_type = self.get_poly_type(poly_type)
		try:
			failed = False 
			temp_export_folder = os.path.join(gom.app.public_directory,'temp_mesh_folder',gom.app.project.user_info_name.split('.txt')[0]) 
			if not os.path.exists(temp_export_folder): 
				os.makedirs(temp_export_folder) 
			for elem in gom.ElementSelection ({'category': ['key', 'elements', 'part', gom.app.project.parts[0], 'explorer_category', 'nominal', 'object_family', 'geometrical_element', 'type', 'inspection_point']}): 
				with open(gom.app.project.user_info_path, 'r') as my_file: 
					lines = my_file.readlines() 
				names = [] 
				for line in lines:
					names.append(line.split(':')[0])
				print(names) 
				if not elem.name in names:
					print('Skipping:',elem.name)
					continue 
				gom.script.cad.show_element_exclusively (elements=[gom.app.project.measurement_series[ms_name]])
					
			
				gom.script.selection3d.select_inside_cube (
					center=gom.app.project.inspection[elem.name], 
					csys=gom.app.project.nominal_elements['system_global_coordinate_system'], 
					height=cube_height, 
					length=cube_length, 
					width=cube_width)
					
				gom.script.sys.edit_creation_parameters (
					element=gom.app.project.parts[0].actual, 
					polygonization_process=poly_type, 
					recalculation_behavior='recalc_without_report_pages')
				
				gom.script.cad.hide_element (elements=[gom.app.project.measurement_series[ms_name]])
				
				gom.script.cad.show_element (elements=[gom.app.project.parts[0].actual])
				
				export_name = os.path.join(temp_export_folder,elem.name + '.g3d')
				
				gom.script.sys.export_g3d (
					color=False, 
					elements=[gom.app.project.parts[0].actual], 
					export_stages_mode='current', 
					file=export_name)
		except Exception as error:
			failed = True 
			self.log.exception( str( error ) )
			curr_time = time.strftime('%H_%M_%S_%m_%d_%Y')
			failed_name = 'FailedToPolygonize_{}'.format(curr_time)
			save_path = os.path.join(Globals.SETTINGS.SavePath, failed_name) 
			gom.script.sys.save_project_as (file_name=save_path)
		return gom.app.project.parts[0].actual
	

	def sn_dict(path): 
		return_dict = {}
		with open(path, 'r') as my_file: 
			lines = my_file.readlines() 
		for line in lines: 
			split_line = line.split(':')
			values = split_line[1].split(',')
			name = split_line[0].strip() 
			sn = values[0].strip() 
			csv = values[1].strip() 
			if csv.upper() == 'TRUE': 
				csv = True 
			else:
				csv = False 
			pdf = values[2].strip() 
			if pdf.upper() == 'TRUE': 
				pdf = True 
			else:
				pdf = False
			return_dict[name] = [sn,csv,pdf] 
		return return_dict
		
	def check_dimensions_oot(): 
		for elem in gom.ElementSelection ({'category': ['key', 'elements', 'part', gom.app.project.parts[0], 'explorer_category', 'inspection']}):
			try:
				if gom.app.project.inspection[elem.name].get ('result_worst_case.out_of_tolerance'): 
					gom.script.sys.set_project_keywords (
						keywords={'failed': 'Fail'}, 
						keywords_description={'failed': 'Part Failed'})
					return True 
			except Exception as err:
				print('Element does not have out of tolerance attribute:',err) 
		gom.script.sys.set_project_keywords (
			keywords={'failed': ''}, 
			keywords_description={'failed': 'Part Failed'})
		return False 

				
		
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
		#Evaluate.EvaluationAnalysis.original__export_results( result )
		curr_time = time.strftime('%H_%M_%S_%m_%d_%Y')
		delete_meshes = True
		work_order = gom.app.project.user_work_order
		inspect_location = gom.app.project.user_inspect_location
		print('Opening template ->',inspect_location) 
		csv_export_path = gom.app.project.user_csv_export_path
		pdf_export_path = gom.app.project.user_pdf_export_path
		info_path = gom.app.project.user_info_path
		info_name = gom.app.project.user_info_name
		meshes_folder = os.path.join(gom.app.public_directory,'temp_mesh_folder',gom.app.project.user_info_name.split('.txt')[0]) 
		meshes_to_import = [] 
		mesh_names = []
		sn_values = PatchedEvaluationAnalysis.sn_dict(info_path) 
		if not os.path.exists(csv_export_path): 
			os.makedirs(csv_export_path) 
		if not os.path.exists(pdf_export_path): 
			os.makedirs(pdf_export_path) 
		for file in os.listdir(meshes_folder): 
			print('->',file)
			if not file.endswith('.g3d'): 
				continue 
			temp = os.path.join(meshes_folder, file) 
			print(temp)
			meshes_to_import.append(temp) 
			mesh_names.append(file.split('.g3d')[0]) 
		gom.script.sys.close_project () 
		gom.script.sys.load_project (
			file=inspect_location, 
			load_working_copy=True) 
		try:
			gom.script.sys.set_project_keywords (
				keywords={'work_order': work_order}, 
				keywords_description={'work_order': 'Work Order Number'})
		except Exception as err:
			print(err) 
		print(meshes_to_import) 
		gom.script.sys.import_g3d (
			files=meshes_to_import, 
			import_mode='clipboard')
		first_elem = True 
		meshes_to_export = gom.ElementSelection ({'category': ['key', 'elements', 'is_element_in_clipboard', 'True', 'explorer_category', 'actual', 'object_family', 'mesh']})[0:]
		for elem in mesh_names: 
			print('->',elem) 

			gom.script.part.add_elements_to_part (
				elements=[gom.app.project.clipboard.actual_elements[elem]], 
				import_mode='replace_elements', 
				part=gom.app.project.parts[0])
			try:
				gom.script.sys.set_project_keywords (
					keywords={'serial_number': sn_values[elem][0]}, 
					keywords_description={'serial_number': 'Serial Number'})
			except Exception as err:
				print(err) 
				
			gom.script.sys.recalculate_project (with_reports=True)
			
			if PatchedEvaluationAnalysis.check_dimensions_oot():
				print('Part Failed!')  
			
			if sn_values[elem][1]: 
				filename = '{}_{}_{}'.format(work_order, sn_values[elem][0], curr_time)
				export_path = os.path.join(csv_export_path, filename + '.csv') 
				try:
					gom.script.table.export_table_contents (
						cell_separator=',', 
						codec='utf-8', 
						decimal_separator='.', 
						elements=gom.ElementSelection ({'category': ['key', 'elements', 'part', gom.app.project.parts[0], 'explorer_category', 'inspection']}), 
						file=export_path, 
						header_export=True, 
						line_feed='\n', 
						sort_column=0, 
						sort_order='descending', 
						template_name='Overview', 
						text_quoting='', 
						write_one_line_per_element=False)
				except Exception as err:
					delete_meshes = False 
					print('Failed to export csv:',err) 
			if sn_values[elem][2]: 
				filename = '{}_{}_{}'.format(work_order, sn_values[elem][0], curr_time)
				export_path = os.path.join(pdf_export_path, filename + '.pdf')  
				try:
					gom.script.report.export_pdf (
						export_all_reports=True, 
						file=export_path, 
						jpeg_quality_in_percent=100)
				except Exception as err:
					delete_meshes = False
					print('Failed to export pdf:',err) 
		if delete_meshes:
			shutil.rmtree(meshes_folder) 
		os.remove(info_path) 
			
class PatchedClient (AsyncClient.Client, metaclass = Utils.MetaClassPatch): 
	def export_results(self, result): 
		PatchedEvaluationAnalysis.export_results(True) 

class NewDefault( DefaultSettings.DefaultSettings, metaclass = Utils.MetaClassPatch ):

	Async = True #Force Async
	AutomaticResultEvaluation = False


if __name__ == '__main__':
	Workflow.start_workflow()



