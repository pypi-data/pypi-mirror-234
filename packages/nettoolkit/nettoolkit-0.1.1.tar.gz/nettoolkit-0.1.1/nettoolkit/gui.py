
import PySimpleGUI as sg

import nettoolkit as nt
from nettoolkit_common.gpl import STR, LOG
from nettoolkit.forms.formitems import *

from nettoolkit.forms.subnet_scanner import subnet_scanner_exec, subnet_scanner_frame, count_ips
from nettoolkit.forms.compare_scanner_outputs import compare_scanner_outputs_exec, compare_scanner_outputs_frame
from nettoolkit.forms.md5_calculator import md5_calculator_exec, md5_calculator_frame
from nettoolkit.forms.pw_enc_dec import pw_enc_cisco_exec, pw_dec_cisco_exec, pw_enc_juniper_exec, pw_dec_juniper_exec, pw_enc_decr_frame
from nettoolkit.forms.prefixes_oper import prefixes_oper_summary_exec, prefixes_oper_issubset_exec, prefixes_oper_pieces_exec, prefixes_oper_frame
from nettoolkit.forms.juniper_oper import juniper_oper_to_jset_exec, juniper_oper_remove_remarks_exec, juniper_oper_frame
from nettoolkit.forms.create_batch import create_batch_exec, create_batch_frame

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class Nettoolkit():
	'''Subnet Scanner GUI - Inititates a UserForm asking user inputs.	'''

	header = 'Nettoolkit - v2.0.1'

	# Object Initializer
	def __init__(self):
		self.tabs_dic = {
			'Subnet Scanner': subnet_scanner_frame(),
			'Compare Scanner Outputs': compare_scanner_outputs_frame(),
			'MD5 Calculate': md5_calculator_frame(),
			'P/W Enc/Dec': pw_enc_decr_frame(),
			'Prefix Operations': prefixes_oper_frame(),
			'Juniper': juniper_oper_frame(),
			'Create Batch': create_batch_frame(),
		}
		self.event_catchers = {
			'go_subnet_scanner': subnet_scanner_exec,
			'go_compare_scanner_outputs': compare_scanner_outputs_exec,
			'go_md5_calculator': md5_calculator_exec,
			'go_pw_enc_cisco': pw_enc_cisco_exec,
			'go_pw_dec_cisco': pw_dec_cisco_exec,
			'go_pw_enc_juniper': pw_enc_juniper_exec,
			'go_pw_dec_juniper': pw_dec_juniper_exec,
			'go_pfxs_summary': prefixes_oper_summary_exec,
			'go_pfxs_issubset' : prefixes_oper_issubset_exec,
			'go_pfxs_break': prefixes_oper_pieces_exec,
			'go_juniper_to_set': juniper_oper_to_jset_exec,
			'go_juniper_remove_remarks': juniper_oper_remove_remarks_exec,
			'go_create_batch': create_batch_exec,
		}
		self.event_updaters = {
			'go_md5_calculator',
			'go_pw_enc_cisco',
			'go_pw_dec_cisco',
			'go_pw_enc_juniper',
			'go_pw_dec_juniper',
			'go_pfxs_summary',
			'go_pfxs_issubset',
			'go_pfxs_break',
		}

		self.create_form()


	def create_form(self):
		"""initialize the form, and keep it open until some event happens.
		"""    		
		layout = [
			banner(self.header + '\tPackage version - ' + nt.version()), 
			self.button_pallete(),
			tabs_display(**self.tabs_dic),
		]
		self.w = sg.Window(self.header, layout, size=(800, 700))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()

			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event in ('Cancel', sg.WIN_CLOSED) : 
				break
			if event in ('Clear',) : 
				self.clear_fields()
				pass
			if event in self.event_catchers:
				if event in self.event_updaters:
					success = self.event_catchers[event](self, i)	
				else:
					success = self.event_catchers[event](i)
				if not success:
					sg.Popup("Mandatory inputs missing or incorrect.\nPlease refill and resubmit.")

			if event == 'go_count_ips':
				self.event_update_element(ss_ip_counts={'value': count_ips(i['pfxs'], i['till'])})

			if event == 'file_md5_hash_check':
				self.event_update_element(file_md5_hash_value={'value': ""})


		self.w.Close()

	def button_pallete(self):
		"""button pallete containing standard OK  and Cancel buttons 

		Returns:
			list: list with sg.Frame containing buttons
		"""    		
		return [sg.Frame(title='Button Pallete', 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[
			[button_cancel("Cancel"),
			sg.Button("Clear", change_submits=True,size=(10, 1), key='Clear'),
			],
		] ), ]

	def event_update_element(self, **kwargs):
		"""update an element based on provided kwargs
		"""    		
		for element, update_values in kwargs.items():
			self.w.Element(element).Update(**update_values)

	def clear_fields(self):
		fields = (
			'op_folder', 'pfxs', 'sockets', 'till', 
			'file1', 'file2',
			'file_md5_hash_check', 'file_md5_hash_value',
			'pw_result_juniper', 'pw_result_cisco', 'pw_cisco', 'pw_juniper',
			'pfxs_summary_input', 'pfxs_summary_result', 'pfxs_subnet', 'pfxs_supernet', 'pfxs_issubset_result', 
				'pfxs_subnet1', 'pfxs_pieces', 'pfxs_pieces_result',
			'file_juniper', 'op_folder_juniper',
			'op_folder_create_batch', 'pfxs_create_batch', 'names_create_batch', 'ips_create_batch',

		)
		for field in fields:
			d = {field:{'value':''}}
			self.event_update_element(**d)


	# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 




# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
	# Test UI #
	# u = Nettoolkit()
	# pprint(u.dic)
	# del(u)

# ------------------------------------------------------------------------------
