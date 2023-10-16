
import PySimpleGUI as sg

def blank_line(): 
	"""to insert a blank row

	Returns:
		list: blank row
	"""		
	return [sg.Text(''),]

def item_line(item, length):
	"""to draw a line with provided character or repeat a character for n-number of time

	Args:
		item (str): character
		length (int): to repeat the character

	Returns:
		list: list with repeated item Text
	"""    	
	return [sg.Text(item*length)]

def under_line(length): 
	"""To draw a line

	Args:
		length (int): character length of line

	Returns:
		list: underline row
	"""		
	return [sg.Text('_'*length)]


def banner(version):
	"""Banner / Texts with bold center aligned fonts

	Args:
		version (str): version of code

	Returns:
		list: list with banner text
	"""    		
	return [sg.Text(version, font='arialBold', justification='center', size=(768,1))] 


def tabs(**kwargs):
	"""create tab groups for provided kwargs

	Returns:
		sg.TabGroup: Tab groups
	"""    		
	tabs = []
	for k, v in kwargs.items():
		tabs.append( sg.Tab(k, [[v]]) )
	return sg.TabGroup( [tabs] )


def button_ok(text, **kwargs):  
	"""Insert an OK button of regular size. provide additional formating as kwargs.

	Args:
		text (str): Text instead of OK to display (if need)

	Returns:
		sg.OK: OK button
	"""		
	return sg.OK(text, size=(10,1), **kwargs)	

def button_cancel(text, **kwargs):
	"""Insert a Cancel button of regular size. provide additional formating as kwargs.

	Args:
		text (str): Text instead of Cancel to display (if need)

	Returns:
		sg.Cancel: Cancel button
	"""    	  
	return sg.Cancel(text, size=(10,1), **kwargs)

def button_pallete():
	"""button pallete containing standard OK  and Cancel buttons 

	Returns:
		list: list with sg.Frame containing buttons
	"""    		
	return [sg.Frame(title='Button Pallete', 
			title_color='blue', 
			relief=sg.RELIEF_RIDGE, 
			layout=[
		[button_ok("Go", bind_return_key=True), button_cancel("Cancel"),],
	] ), ]

def get_list(raw_items):
	"""create list from given raw items splits by enter and comma

	Args:
		raw_items (str): multiline raw items

	Returns:
		list: list of items
	"""	
	ri_lst = raw_items.split("\n")
	lst = []
	for i, item in enumerate(ri_lst):
		if item.strip().endswith(","):
			ri_lst[i] = item[:-1]
	for ri_item in ri_lst:
		lst.extend(ri_item.split(","))
	for i, item in enumerate(lst):
		lst[i] = item.strip()		
	return lst



def tabs_display(**tabs_dic):
	"""define tabs display

	Returns:
		list: list of tabs
	"""    		
	return [tabs(**tabs_dic),]

