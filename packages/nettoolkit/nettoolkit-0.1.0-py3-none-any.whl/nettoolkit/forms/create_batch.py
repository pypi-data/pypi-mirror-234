
import PySimpleGUI as sg

from nettoolkit.forms.formitems import *
from nettoolkit.batch import create_batch_file

def create_batch_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if (i['ips_create_batch'] != "" 
			and i['pfxs_create_batch'] != "" 
			and i['names_create_batch'] != "" 
			and i['op_folder_create_batch'] != ""
			):
			ips_create_batch = get_list(i['ips_create_batch'])
			pfxs_create_batch = get_list(i['pfxs_create_batch'])
			names_create_batch = get_list(i['names_create_batch'])
			for ip in ips_create_batch:
				success = create_batch_file(pfxs_create_batch, names_create_batch, ip, i['op_folder_create_batch'])
			if success:
				s = 'batch file creation process complete. please verify'
				print(s)
				sg.Popup(s)
			else:
				s = 'batch file creation process encounter errors. please verify inputs'
				print(s)
				sg.Popup(s)
			return True
	except:
		return None

def create_batch_frame():
	"""tab display - create batch file

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Ping-batch file(s) create', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('output folder:', text_color="yellow"), 
			sg.InputText('', key='op_folder_create_batch'),  
			sg.FolderBrowse(),
		],
		[sg.Column([
			[sg.Text("Prefixes", text_color="yellow"),],
			[sg.Multiline("", key='pfxs_create_batch', autoscroll=True, size=(25,10), disabled=False),],
			[sg.Text("Example: \n10.10.10.0/24\n10.10.30.0/24,10.10.50.0/25")],

			]),
		sg.Column([
		[sg.Text("Prefix Names", text_color="yellow")],
		[sg.Multiline("", key='names_create_batch', autoscroll=True, size=(25,10), disabled=False) ],
		[sg.Text("Example: \nVlan-1\nVlan-2,Loopback0")],

			]),
		sg.Column([
			[sg.Text("IP(s)", text_color="yellow")],
			[sg.Multiline("", key='ips_create_batch', autoscroll=True, size=(10,10), disabled=False) ],
			[sg.Text("Example: \n1\n3,4,5")],

			]),

		],
		under_line(80),
		[sg.Text("Entries of Prefixes and Prefix Names should match exactly")],
		[sg.Text("Entries can be line(Enter) or comma(,) separated")],
		under_line(80),
		[sg.Button("Create", size=(10,1),  change_submits=True, key='go_create_batch')],
		under_line(80),

		])


