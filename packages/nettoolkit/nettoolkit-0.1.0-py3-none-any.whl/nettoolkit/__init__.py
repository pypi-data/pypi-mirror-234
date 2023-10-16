__doc__ = '''Networking ToolSet
'''

__all__ = [
	# .addressing
	'IPv4', 'IPv6', 'addressing', 'Validation', 'get_summaries', 'isSubset',
	'binsubnet', 'bin2dec', 'bin2decmask', 'to_dec_mask', 'bin_mask', 'Routes', 'invmask_to_mask',

	#batch
	"CreateBatch", "create_batch_file",

	# common
	"remove_domain", "read_file", "get_op", "blank_line", "get_device_manufacturar", "verifid_output", 
	"get_string_part", "get_string_trailing", "standardize_mac", "mac_2digit_separated", "mac_4digit_separated", 
	"flatten", "dataframe_generate",

	#gui
	"Nettoolkit",

	#subnetscan
	"compare_ping_sweeps", "Ping",

	]

__version__ = "0.1.0"

from .addressing import (
	IPv4, IPv6, addressing, Validation, get_summaries, isSubset,
	binsubnet, bin2dec, bin2decmask, to_dec_mask, bin_mask, Routes, invmask_to_mask,
	)
from .batch import CreateBatch, create_batch_file
from .common import (
	remove_domain, read_file, get_op, blank_line, get_device_manufacturar, verifid_output, 
	get_string_part, get_string_trailing, standardize_mac, mac_2digit_separated, mac_4digit_separated,
	flatten, dataframe_generate
	)
from .gui import Nettoolkit
from .subnetscan import compare_ping_sweeps, Ping


def version():
	return __version__