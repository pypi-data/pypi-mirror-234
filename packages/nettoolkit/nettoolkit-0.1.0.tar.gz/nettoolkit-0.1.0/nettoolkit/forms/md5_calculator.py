
import PySimpleGUI as sg

from nettoolkit.forms.formitems import *
from pyJuniper import get_md5



def md5_calculator_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['file_md5_hash_check'] != '':
			obj.event_update_element(file_md5_hash_value={'value': "calculating..."})
			_hash = get_md5(i['file_md5_hash_check'])
			obj.event_update_element(file_md5_hash_value={'value': _hash})	
			return True
	except:
		return None

def md5_calculator_frame():
	"""tab display - MD5 Calculator

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('MD5 Calculator', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Select file:', text_color="yellow"), 
			sg.InputText(key='file_md5_hash_check', change_submits=True),  
			sg.FileBrowse()],
		under_line(80),

		[sg.Text('Generated MD5 Hex:',  text_color="dark green"), 
			sg.InputText(key='file_md5_hash_value', disabled=True), ],
		under_line(80),

		[sg.Button("Start", change_submits=True, key='go_md5_calculator')],

		])
