

import PySimpleGUI as sg
from nettoolkit_common.gpl import STR, LOG

from nettoolkit import addressing
from nettoolkit.forms.formitems import *
from nettoolkit.subnetscan import Ping


def subnet_scanner_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['op_folder'] != '' and i['pfxs'] != "":
			file = 'ping_scan_result_'
			op_file = f"{STR.get_logfile_name(i['op_folder'], file, ts=LOG.time_stamp())[:-4]}.xlsx"
			pfxs = get_list(i['pfxs'])
			try:
				concurrent_connections = int(i['sockets'])
			except:
				concurrent_connections = 1000
			#
			P = Ping(pfxs, i['till'], concurrent_connections, i['subnet_scanner_create_tabs'])
			P.op_to_xl(op_file)
			sg.Popup("Scan completed, \nFile write completed, \nVerify output")
			return True
	except:
		return None

def subnet_scanner_frame():
	"""tab display - subnet scanner

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('IP Subnet Scanner', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('select output folder :',  text_color="yellow"), 
			sg.InputText('', key='op_folder'),   sg.FolderBrowse(),
		],

		[sg.Text("Prefixes - enter/comma separated", text_color="yellow")],
		[sg.Multiline("", key='pfxs', autoscroll=True, size=(30,14), disabled=False) ],
		[sg.Button("Count_ips", change_submits=True, key='go_count_ips'), sg.Text('', key="ss_ip_counts") ],

		[sg.Text('[n]', text_color="yellow"), sg.InputCombo(list(range(1,256)), key='till', size=(20,1)),  
		sg.Text('Concurrent connections', text_color="yellow"), sg.InputText(1000, key='sockets', size=(20,1))],  
		under_line(80),

		[sg.Checkbox('create separate tab for each subnet', key='subnet_scanner_create_tabs', default=False, text_color='yellow')],
		under_line(80),

		[sg.Button("Start", change_submits=True, key='go_subnet_scanner')],
		])


def count_ips(pfxs, till):
	"""counts ips for given subnets / prefixes

	Args:
		pfxs (list): list of prefixes
		till (integer): number till count

	Returns:
		int: number of total ips in given prefixes
	"""	
	try:
		count = 0
		if not pfxs: return count
		hostlist = []
		pfxs = get_list(pfxs)
		for pfx in pfxs:
			subnet = addressing(pfx)
			try:
				if till:
					hosts = subnet[1:int(till)+1]
				else:
					hosts =subnet[0:len(subnet)]
			except:
				hosts =subnet[0:len(subnet)]
			hostlist.extend([host for host in hosts])
		count = len(set(hostlist))
		return count
	except:
		pass
