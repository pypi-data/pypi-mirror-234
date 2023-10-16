"""cisco running-config - ip routes output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict

from facts_finder.generators.commons import *
from .common import *

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningRoutes():
	"""object for running config routes parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		
		self.cmd_op = verifid_output(cmd_op)
		self.route_dict = {}

	def route_read(self, func):
		"""directive function to get the various routes level output

		Args:
			func (method): method to be executed on ip routes config line

		Returns:
			dict: parsed output dictionary
		"""    		
		n = 0
		ports_dict = OrderedDict()
		for l in self.cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("!"): continue
			if not l.startswith("ip route ") and not l.startswith("ipv6 route "): continue
			#
			spl = l.strip().split()
			n += 1
			ports_dict[n] = {}
			rdict = ports_dict[n]
			rdict['filter'] = 'static'
			func(rdict,  l, spl)
		return ports_dict

	def routes_dict(self):
		"""update the route details
		"""   
		func = self.get_route_dict
		merge_dict(self.route_dict, self.route_read(func))

	@staticmethod
	def get_route_dict(dic, l, spl):
		"""parser function to update route details

		Args:
			dic (dict): blank dictionary to update a route info
			l (str): line to parse

		Returns:
			None: None
		"""
		version = 'unknown'		
		if spl[0] == 'ip': version = 4
		if spl[0] == 'ipv6': version = 6
		#
		idx_update = 0
		pfx_vrf = ''
		if spl[2] == 'vrf': 
			pfx_vrf = spl[3]
			idx_update += 2
		#
		if version == 4:
			prefix, subnet_mask, next_hop = spl[idx_update+2], spl[idx_update+3], ''
			prefix = inet_address(prefix, subnet_mask)
			nh = spl[idx_update+4]
			try:
				addressing(nh)
				next_hop = nh
				idx_update += 1
			except:
				pass
		elif version == 6:
			prefix, next_hop = spl[idx_update+2], ''
			nh = spl[idx_update+3]
			idx_update -= 1
			try:
				addressing(nh)
				next_hop = nh
				idx_update += 1
			except:
				pass
		else:
			return None
		#
		adminisrative_distance = ''

		if 'Null0' in spl:
			if spl[idx_update+5].isnumeric():
				adminisrative_distance = spl[idx_update+5]
				idx_update += 2
			else:
				idx_update += 1
		elif next_hop != '' and len(spl)>=idx_update+5 and spl[idx_update+4].isnumeric():
			adminisrative_distance = spl[idx_update+4]
			idx_update += 1
		#
		tag_value = ''
		if 'tag' in spl:
			tag_value = spl[idx_update+5]
			idx_update += 2
		#
		remark = ''
		if 'name' in spl:
			remark = " ".join(spl[idx_update+5:])
			idx_update += 2
		#
		dic['pfx_vrf'] = pfx_vrf
		dic['prefix'] = prefix
		dic['next_hop'] = next_hop
		dic['adminisrative_distance'] = adminisrative_distance
		dic['tag_value'] = tag_value
		dic['remark'] = remark
		dic['version'] = version
		return dic



# ------------------------------------------------------------------------------


def get_system_running_routes(cmd_op, *args):
	"""defines set of methods executions. to get various ip route parameters.
	uses RunningRoutes in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""
	R  = RunningRoutes(cmd_op)
	R.routes_dict()


	# # update more interface related methods as needed.
	if not R.route_dict:
		R.route_dict['dummy_col'] = ""

	return R.route_dict

# ------------------------------------------------------------------------------

