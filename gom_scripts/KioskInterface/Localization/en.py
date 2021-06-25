# -*- coding: utf-8 -*-
# Script: Definition of all messages for localization
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
# 2015-05-18: Descriptions of default project keywords added.

from KioskInterface.Base.Misc import Messages


class Localization( Messages.Localization ):

	msg_general_failure_title = 'Failure'
	msg_global_failure_text = 'Unexpected Failure: '

	msg_evaluate_process_text = '{0} of {1} Measurement steps'
	msg_evaluate_detail_msg_initialize = 'Initialize'
	msg_evaluate_detail_msg_reports = 'Update Reports'
	msg_evaluate_detail_msg_recalc = 'Recalculate Project'
	msg_evaluate_detail_msg_polygonize = 'Polygonize'
	msg_evaluate_detail_msg_photogrammetry = 'Photogrammetry'
	msg_evaluate_detail_msg_digitizing = 'Digitizing'
	msg_evaluate_detail_msg_safety_home = 'Using validated path to home'
	msg_evaluate_detail_calibrate = 'Calibrate'
	msg_evaluate_estimated_time = 'Estimated measurement execution time {} minutes left'

	msg_async_failure_title = 'Communication Failure'
	msg_async_failure_start_server = 'Failed to start Communication Server'
	msg_async_failure_communicate_client = 'Failed to communicate with AsyncClient'
	msg_async_client_process_working = 'Working on Project {}'
	msg_async_client_process_finished = 'Finished Project {}'
	msg_async_client_result = 'Part ID {0}: checked {1} elements, {2} elements uncomputed and {3} elements outside tolerance'

	msg_system_configuration_failed_title = 'System Configuration Check'
	msg_no_measurement_list = 'No compatible measurement series in template'
	msg_no_measurement_list_real = '<b>Connected hardware:</b>'
	msg_calibration_failed_execute = 'Failed to perform calibration series.'
	msg_calibration_no_list_defined = 'No Calibration Measurement Series defined'
	msg_photogrammetry_no_list_defined = 'No photogrammetry measurement series defined'
	msg_photogrammetry_verification_failed = 'Photogrammetry measurement verification failed.'
	msg_photogrammetry_failed_execute = 'Failed to excecute Photogrammetry series'
	msg_digitizing_no_list_defined = 'No digitizing measurement series defined'
	msg_digitizing_failed_execute = 'Failed to excecute Measurement series'
	msg_digitizing_failed_maxrepetitions = 'Failed to perform digitize measurement'
	msg_digitizing_failed_already_calibrated = 'Failed to perform digitize measurement.<br/>Calibration already performed.'
	msg_sensor_failed_init = 'Failed to initialize sensor'
	msg_sensor_failed_warmup = 'Failed to wait for sensor warmup'
	msg_msetup_sensor_offline = 'Sensor is uninitialized'
	msg_msetup_define_active_failed = 'Measuring setup could not be activated'
	msg_safely_move_failed = 'Failed to safely move to home position'
	msg_sensor_warning = 'ATOS ScanBox warning:<br/>{}'
	msg_evaluate_failed_home_check_series = 'Aborting Evaluation, its only possible to execute measurement series which start and end with an home position'
	msg_calibration_too_often = 'Calibration was already performed<br/>next possible Calibration in {}'
	msg_userabort = 'User abort'
	msg_verification_failed = 'Measurement verification failed'
	msg_verification_transformation_exception = 'Aborting due to transformation error.'
	msg_verification_temperature_exception = 'Aborting due to temperature difference error.'
	msg_verification_move_light_exception = 'Aborting due to movement/lighting error.'
	msg_verification_scale_bar_identify = 'Failed to identify scale bars'
	msg_verification_no_scan_data = 'No measurements with scandata found'
	msg_verification_refpointmismatch = 'Alignment residual difference was exceeded.<br/>Photogrammetry does not match digitizing measurements!'
	msg_emergency_button = 'Emergency Button pressed.'
	msg_multi_comprehensive_retries_exceeded = 'Number of retries for comprehensive photogrammetry exceeded.'
	msg_reverse_move_not_allowed = 'After emergency stop: This device does not allow a reverse move to home position.'

	msg_verification_transformation_failed = 'Transformation Limit failed in {0} measurements.<br/>Only {1} are allowed.'
	msg_burnin_transformation_failed = 'Transformation Limit (Burn-In) failed in {0} measurements.<br/>Only {1} are allowed.'
	msg_verification_projector_residual_failed = 'Projector Residual Limit failed in {0} measurements.<br/>Only {1} are allowed.'
	msg_burnin_projector_residual_failed = 'Projector Residual Limit (Burn-In) failed in {0} measurements.<br/>Only {1} are allowed.'
	msg_verification_movement_check_failed = 'Movement Check Limit failed in {0} measurements.'
	msg_verification_lighting_failed = 'Lighting Check Limit failed in {0} measurements.'
	msg_verification_intersection_failed = 'Intersection Check Limit failed in {0} measurements.'
	msg_burnin_preview_points_failed = 'Number of Preview Points Limit (Burn-In) failed in {0} measurements.<br/>Only {1} are allowed.'
	msg_verification_global_digitize_failed = 'Failed to verify measurement alignment'
	msg_verification_global_digitize_too_large = 'Measurement alignment residual is too large.'
	msg_verification_unrecoverable_position = 'Unrecoverable robot position detected'
	msg_verification_calibration_failed = 'Failed to verify calibration.'


	startdialog_label_title = '<p style="font-size: 48px">Welcome</p>'
	startdialog_label_user = 'User:'
	startdialog_label_serial = 'Serial:'
	startdialog_label_fixture = 'Fixture:'
	startdialog_label_template = 'Template:'
	startdialog_button_template = 'Choose'
	startdialog_button_start = 'Start'
	startdialog_button_exit = 'Exit'
	multipart_wizard_button_next = 'Next'
	multipart_wizard_button_prev = 'Prev'
	multipart_wizard_label_title = '<p style="font-size: 32px">Fill in serials<br>and choose templates</p>'
	multipart_wizard_label_page = 'Page {} of {}'
	multipart_waitdialog_title = '<p align="center">Adapt the measuring setup for template<br/>{}</p>'
	multipart_waitdialog_button_ok = 'OK'
	multipart_waitdialog_button_cancel = 'Cancel'

	progessdialog_label_title = 'Wait until the measurement is completed'
	progressdialog_multipart_label = 'Total number of projects'
	confirmdialog_label_title = '<p style="font-size: 48px">Approve Component</p>'
	confirmdialog_label_instruction = '<p style="font-size: 32px">Do you want to accept the measurement?</p>'
	confirmdialog_button_approve = 'Approve'
	confirmdialog_button_reject = 'Reject'

	errordialog_button_retry = 'Retry'
	errordialog_button_abort = 'Abort'
	errordialog_button_close = 'Close'
	errordialog_button_gomsic = 'GOMSic'
	errordialog_button_continue = 'Continue'

	waitdialog_title = 'Please Wait'
	waitdialog_client_setup = 'Setting up clients.'
	waitdialog_clients_exit = 'Wait for clients to exit'

	measuring_setup_title = '<p align="center">Make sure the measurement setup<br/>is ready for measurement series:</p>'
	measuring_setup_button_ok = 'OK'
	measuring_setup_button_cancel = 'Cancel'
	temperature_title = '<p align="center" style="font-size: 32px">Enter current temperature in °C</p>'
	temperature_button_ok = 'OK'
	temperature_button_cancel = 'Cancel'
	msg_common_refpoint_trafo_less_points = 'Transform by common reference points failed: less than three points found!'
	msg_common_refpoint_trafo_error = 'Transform by common reference points failed: {}'

	msg_cannot_execute = 'Not possible to evaluate this project: no VMR, or not all measurements have recorded positions!'

	msg_setting_invalid = 'Unexpected Failure: invalid setting {}'
	msg_settings_savepath_failed = 'Failed to create save path folder "{}"<br/>Please contact your administrator and start the setup script which can be found within the script database'

	msg_platform_not_supported = 'Only the Windows platform is supported!'
	msg_only_with_atos_onlinemode = 'Only the ATOS software supports online mode!'

	msg_barcode_connectionfailed = 'Failed to communicate with BarCode Scanner on port COM{}'
	
	msg_disc_space_warning = 'Disc space warning limit reached!<br/>Only {}MB free in {}'
	msg_disc_space_error = 'Disc space error limit reached!<br/>Only {}MB free in {}'
	msg_save_error_title = 'Final project save failed'
	msg_save_error_message = 'Not enough disc space for the evaluated project.'

	project_consistency_title = 'Invalid project template'
	project_consistency_report_alignments = '<b>Used alignments in reports:</b>'
	project_consistency_required_alignments = '<b>Alignments required:</b>'
	project_consistency_vmr = '<b>VMR:</b>'
	project_consistency_measuring_setups = '<b>Measuring setups:</b>'
	project_consistency_path_status = '<b>Path status:</b>'
	project_consistency_vmr_measurement_series = '<b>VMR measurement series:</b>'
	project_consistency_report_status = '<b>Report status:</b>'
	project_consistency_measurement_status = '<b>Measurement parameters:</b>'
	project_consistency_photogrammetry = '<b>Photogrammetry:</b>'
	project_consistency_nco = '<b>Elements in clipboard:</b>'
	project_consistency_non_master_actual_data = '<b>Elements with actual data are kept:</b>'
	project_part_based_error = 'It is not possible to execute a part based project template.'

	keyword_description_user = 'Inspector'
	keyword_description_serial = 'Part no.'
	keyword_description_fixture = 'Fixture no.'
	keyword_description_date = 'Date'
	
	statusbar_text_multipart_progress = '<center>Performing measurement {} of {}</center>'
	
	msg_no_atos_inline_license = 'ATOS Inline license is needed!'

