"""cisco show cdp neighbour command output parser """

# ------------------------------------------------------------------------------

from facts_finder.generators.commons import *
from .common import *
# ------------------------------------------------------------------------------

def get_cdp_neighbour(cmd_op, *args, dsr=True):
	"""parser - show cdp neigh command output // Deprycated and removed // use lldp neighbor instead.

	Parsed Fields:
		* port/interface
		* neighbor interface
		* neighbor plateform
		* neighbor hostname

	Args:
		cmd_op (list, str): command output in list/multiline string.
		dsr (bool, optional): DOMAIN SUFFIX REMOVAL. Defaults to True.

	Returns:
		dict: output dictionary with parsed fields
	"""	
	cmd_op = verifid_output(cmd_op)
	nbr_d, remote_hn, prev_line = {}, "", ""
	nbr_table_start = False
	for i, line in enumerate(cmd_op):
		line = line.strip()
		if line.startswith("Device ID"): 
			nbr_table_start = True
			continue
		if not nbr_table_start: continue
		if not line.strip(): continue				# Blank lines
		if line.startswith("Total "): continue		# Summary line
		if line.startswith("!"): continue			# Remarked line

		### NBR TABLE PROCESS ###

		if len(line.strip().split()) == 1:  
			prev_line = line
			continue
		if prev_line:
			l = prev_line.strip() + " " + line
			prev_line = ""
		else:
			l = line
		dbl_spl = l.split("  ")

		# // NBR HOSTNAME //
		if not remote_hn:
			remote_hn = dbl_spl[0].strip()
			if dsr: remote_hn = remove_domain(remote_hn)

		# // LOCAL/NBR INTERFACE, NBR PLATFORM //
		local_if = STR.if_standardize("".join(dbl_spl[0].split()))
		remote_if = STR.if_standardize("".join(dbl_spl[-1].split()[1:]))
		remote_plateform = dbl_spl[-1].split()[0]

		# SET / RESET
		nbr_d[local_if] = {'nbr': {}}
		nbr = nbr_d[local_if]['nbr']
		nbr['hostname'] = remote_hn
		nbr['interface'] = remote_if
		nbr['plateform'] = remote_plateform
		remote_hn, remote_if, remote_plateform = "", "", ""
	return nbr_d
# ------------------------------------------------------------------------------
