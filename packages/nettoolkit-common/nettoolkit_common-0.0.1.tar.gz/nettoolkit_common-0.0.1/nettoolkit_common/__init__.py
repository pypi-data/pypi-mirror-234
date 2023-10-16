__doc__ = '''Networking Tool Set Common Functions
'''


__all__ = [
	# .gpl
	'Default', 'Container', 'Numeric', 'DifferenceDict', 
	'STR', 'IO', 'LST', 'DIC', 'LOG', 'DB', 'IP', 'XL_READ', 'XL_WRITE', 
	'DictMethods', 'Multi_Execution', 'nslookup', 'standardize_if', 'get_username', 'get_password', 
	'get_juniper_int_type', 'get_cisco_int_type',
	]


__version__ = "0.0.1"


from .gpl import (Default, Container, Numeric, 
	DifferenceDict, DictMethods, DIC,
	STR, IO, LST, LOG, DB, IP, XL_READ, XL_WRITE, 
	Multi_Execution, nslookup, standardize_if,
	get_username, get_password, 
	get_juniper_int_type, get_cisco_int_type
	)


def version():
	return __version__