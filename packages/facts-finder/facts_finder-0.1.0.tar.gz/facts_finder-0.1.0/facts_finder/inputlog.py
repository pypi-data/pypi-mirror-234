# ------------------------------------------------------------------------------------------------
from pathlib import *

# ------------------------------------------------------------------------------------------------

CISCO_BANNER = """!================================================================================
! output for command: COMMAND 
!================================================================================
"""
JUNIPER_BANNER = """#================================================================================
# output for command: COMMAND 
#================================================================================
"""

# ------------------------------------------------------------------------------------------------

def get_hostname(lines):
	cmds = {
		'show configuration', 'show version', 'show interfaces terse',
		'sh ver', 'sh run', 'sh int status', 'sh int desc',
	}
	for line in lines:		
		if line.strip().startswith('hostname') or line.strip().startswith('host-nmae'):
			return line.strip().split('name')[-1].strip()

		elif line.find("#") > -1 or line.find(">") > -1:
			for cmd in cmds:
				if line.find(cmd) > 1:
					return line.split(cmd)[0].split("@")[-1].strip()[:-1]


def get_model(lines):
	for line in lines:
		if line.strip().startswith("!"): return 'cisco'
		if line.strip().startswith("#"): return 'juniper'


def get_cmd_lines_cisco(lines, hostname, model):
	cmd_dict = {}
	for i, line in enumerate(lines):
		if not line.find(hostname)>-1: continue
		si = line.find(hostname)
		cmd_begin_i = si + len(hostname)
		cmd = line[cmd_begin_i:].strip()
		if cmd[1:] and cmd[0] in(">", "#"):# and not cmd.endswith("?"):
			cmd_dict[i] = cmd[1:].strip()

	return cmd_dict

def get_output_lines_list(lines, startidx, endidx):
	return lines[startidx:endidx]

def is_valid_op(lines):
	# print(lines[0].strip().startswith("^"))
	return lines and not lines[0].strip().startswith("^")


def get_banner(model, cmd):
	banner = ""
	if model == 'cisco': 
		banner = CISCO_BANNER.replace("COMMAND", cmd)
	if model == 'juniper': 
		banner = JUNIPER_BANNER.replace("COMMAND", cmd)
	return banner

def trim_hostname_lines(cmd_output_lines_list, hostname):
	return [ line
		for line in cmd_output_lines_list
			if not (line.find(hostname+"#")>-1 
				 or line.find(hostname+">")>-1 
				 or line.startswith('{master:')
				)
	]


def create_new_file(op_file):
	with open(op_file, 'w') as f:
		f.write("")

def get_idx_tuples(sorted_idx, cmd_lines_idx):
	idx_tuples = []
	for i, endidx in enumerate(sorted_idx):
		if i == 0: 
			startidx = endidx+1
			continue
		# cmd = cmd_lines_idx[sorted_idx[i-1]]
		idx_tuples.append((startidx, endidx))
		startidx = endidx+1
	return idx_tuples

def convert_and_write(op_file, lines, hostname, model):

	cmd_lines_idx = get_cmd_lines_cisco(lines, hostname, model)
	sorted_idx = sorted(cmd_lines_idx)
	sorted_idx.append(len(lines))
	create_new_file(op_file)
	idx_tuples = get_idx_tuples(sorted_idx, cmd_lines_idx)
	for s, e in idx_tuples:
		cmd = cmd_lines_idx[s-1]
		if cmd.endswith("?"): continue
		banner = get_banner(model, cmd)
		cmd_output_lines_list = get_output_lines_list(lines, s, e)
		cmd_output_lines_list = trim_hostname_lines(cmd_output_lines_list, hostname)
		valid_op = is_valid_op(cmd_output_lines_list)
		s = ""
		if valid_op:
			s += banner
			s += "".join(cmd_output_lines_list)
			with open(op_file, 'a') as f:
				f.write(s)


def is_cit_file(lines):
	for line in lines:
		if line[1:].startswith(" output for command:"):
			return True
	return False

def to_cit(input_log):
	p = Path(input_log)
	previous_path = p.resolve().parents[0]
	with open(input_log, 'r') as f:
		lines = f.readlines()
	hostname = get_hostname(lines)
	output_log = f"{previous_path}/{hostname}.log"
	output_bkp_log = f"{previous_path}/{hostname}-bkp.log"
	if input_log == output_log:
		with open(output_bkp_log, 'w') as f:
			f.write("".join(lines))
	model = get_model(lines)
	if is_cit_file(lines):
		return input_log
	convert_and_write(output_log, lines, hostname, model)
	return output_log


# ------------------------------------------------------------------------------------------------
#   MAIN
# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	pass
	#
	path = 'c:/users/al202t/OneDrive - AT&T Services, Inc/Desktop'
	file = f'{path}/j.log'
	file = f'{path}/c.log'
	to_cit(file)
# ------------------------------------------------------------------------------------------------


