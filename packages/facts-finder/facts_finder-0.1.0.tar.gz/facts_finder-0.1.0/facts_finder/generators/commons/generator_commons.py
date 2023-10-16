
from nettoolkit_common.gpl import *
from nettoolkit_common import *
from nettoolkit_db import *
from nettoolkit.addressing import *
from pyNetCrypt import *
from pyJuniper import *

# ================================================================================================
# common functions
# ================================================================================================

def get_appeneded_value(dic, key, value):
	"""appends the value to an existing value found in dictionary with provided key if exist other wise returns same value

	Args:
		dic (dict): dictionary
		key (str): dictionary key
		value (str): arbitrary value to be appended to existing key if exist

	returns:
		str: appened string
	"""
	if not dic.get(key):
		return value
	else:
		return dic[key] + '\n'+ value

def add_to_list(lst, item):
	"""appends item to list if not found

	Args:
		lst (list): list
		item (str, int): item to be added to list

	Returns:
		list: updated list
	"""	
	if item in lst:
		return lst
	return lst.append(item)

# ================================================================================================

def get_subnet(address):
	"""derive subnet number for provided ipv4 address

	Args:
		address (str): ipv4 address in string format a.b.c.d/mm

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv4(address).subnet_zero()

def get_v6_subnet(address):
	"""derive subnet number for provided ipv6 address

	Args:
		address (str): ipv6 address in string with mask

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv6(address).subnet_zero()


def get_int_ip(ip): 
	"""get ip address from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: ip address
	"""	
	return ip.split("/")[0]

def get_int_mask(ip): 
	"""get mask from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: mask
	"""	
	return ip.split("/")[-1]

