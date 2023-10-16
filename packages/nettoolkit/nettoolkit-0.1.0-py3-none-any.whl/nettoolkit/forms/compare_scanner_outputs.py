
import PySimpleGUI as sg

from nettoolkit.forms.formitems import *
from nettoolkit.subnetscan import compare_ping_sweeps


def compare_scanner_outputs_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['file1'] != '' and i['file2'] != '':
			compare_ping_sweeps(i['file1'], i['file2'])
			return True
	except:
		return None

def compare_scanner_outputs_frame():
	"""tab display - Compares output of scanner and result

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Compare - IP Scanner Output files', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Select first scanner file :',  text_color="yellow"), 
			sg.InputText(key='file1'),  
			sg.FileBrowse()],
		under_line(80),

		[sg.Text('Select second scanner file :',  text_color="yellow"), 
			sg.InputText(key='file2'),  
			sg.FileBrowse()],
		under_line(80),
		[sg.Button("Start", change_submits=True, key='go_compare_scanner_outputs')],

		])

