import PySimpleGUI as sg

from nettoolkit.forms.formitems import *
from nettoolkit.addressing import get_summaries, addressing, isSubset


def prefixes_oper_summary_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['pfxs_summary_input'] != '':
			obj.event_update_element(pfxs_summary_result={'value': "calculating..."})
			_summaries = get_summaries(*get_list(i['pfxs_summary_input']))
			obj.event_update_element(pfxs_summary_result={'value': "\n".join([ str(p) for p in _summaries])})	
			return True
	except:
		return None

def prefixes_oper_issubset_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['pfxs_subnet'] != '' and i['pfxs_supernet'] != '':
			obj.event_update_element(pfxs_issubset_result={'value': "checking..."})
			result = isSubset(i['pfxs_subnet'], i['pfxs_supernet'])
			if result:
				obj.event_update_element(pfxs_issubset_result={'value': 'Yes', 'text_color': "green" })	
			else:
				obj.event_update_element(pfxs_issubset_result={'value': 'No', 'text_color': "red" })	
			return True
	except:
		return None

def prefixes_oper_pieces_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['pfxs_subnet1'] != '' and i['pfxs_pieces'] != '':
			obj.event_update_element(pfxs_pieces_result={'value': "checking..."})
			ipobj = addressing(i['pfxs_subnet1'])
			result = ipobj / int(i['pfxs_pieces'])
			obj.event_update_element(pfxs_pieces_result={'value': "\n".join([ str(p) for p in result])})	
			return True
	except:
		return None



def prefixes_oper_frame():
	"""tab display - Prefix Operations

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Prefix Operations', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Summarize Prefixes', text_color="black"), ],
		[sg.Multiline("", key='pfxs_summary_input', autoscroll=True, size=(30,14), disabled=False),
		sg.Text('}}', text_color="black"),
		sg.Multiline("", key='pfxs_summary_result', autoscroll=True, size=(30,14), disabled=True), ],
		[sg.Button("Summarize", size=(10,1),  change_submits=True, key='go_pfxs_summary')],

		[sg.Column([
			under_line(38),
			[sg.Text('Verify: is Subnet part of Supernet ?', text_color="black"), ],
			[sg.Text('   Subnet:', text_color="yellow"), 
			sg.InputText(key='pfxs_subnet', size=(15,1)),], 
			[sg.Text('Supernet:', text_color="yellow"), 
			sg.InputText(key='pfxs_supernet', size=(15,1)),], 
			[sg.Button("Check", size=(10,1), change_submits=True, key='go_pfxs_issubset')],
			[sg.Text('    Result:', text_color="black"),
			sg.InputText('', key='pfxs_issubset_result' , size=(5,1),  text_color="black")], 
			under_line(38),
			]),
		sg.Column([
			under_line(38),
			[sg.Text('Break Your Subnet (equal pieces)', text_color="black"), ],
			[sg.Text('Subnet:', text_color="yellow"), 
			sg.InputText(key='pfxs_subnet1', size=(15,1)),
			sg.Text('/n:', text_color="yellow"), sg.InputCombo(list(range(1,256)), key='pfxs_pieces', size=(4,1)),],
			[sg.Button("Break", size=(10,1), change_submits=True, key='go_pfxs_break')],
			[sg.Text('Result:', text_color="black"),
			sg.Multiline("", key='pfxs_pieces_result', autoscroll=True, size=(20,3), disabled=True),], 
			under_line(38),
			]),
		],
		])

