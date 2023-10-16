

import PySimpleGUI as sg
from pathlib import *
import sys

from nettoolkit.forms.formitems import *
from pyJuniper.juniper import Juniper


def juniper_oper_to_jset_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['file_juniper'] != '' and i['op_folder_juniper'] != '':
			p = Path(i['file_juniper'])
			input_file = p.name
			output_file = i['op_folder_juniper'] + '/' + ".".join(input_file.split(".")[:-1]) + '.set.txt'
			J = Juniper(i['file_juniper'], output_file)    # define a Juniper Object
			s = J.convert_to_set(to_file=True)      # convert the Juniper config to set mode.
			return True
	except:
		return None

def juniper_oper_remove_remarks_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['file_juniper'] != '' and i['op_folder_juniper'] != '':
			p = Path(i['file_juniper'])
			input_file = p.name
			output_file = i['op_folder_juniper'] + '/' + ".".join(input_file.split(".")[:-1]) + '.-remarks.txt'
			J = Juniper(i['file_juniper'], output_file)    # define a Juniper Object
			s = J.remove_remarks(to_file=True)      #  remove remarks from config
			return True
	except:
		return None



def juniper_oper_frame():
	"""tab display - Juniper Operations

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Juniper Operations', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Select Juniper Config file :',  text_color="yellow"), 
			sg.InputText(key='file_juniper'),
			sg.FileBrowse()],

		[sg.Text('select output folder :',  text_color="yellow"), 
			sg.InputText('', key='op_folder_juniper'),   sg.FolderBrowse(),
		],
		under_line(80),

		[sg.Button("Convert to Set", size=(20,1),  change_submits=True, key='go_juniper_to_set')],
		[sg.Button("Remove Remarks", size=(20,1),  change_submits=True, key='go_juniper_remove_remarks')],
		under_line(80),

		])

