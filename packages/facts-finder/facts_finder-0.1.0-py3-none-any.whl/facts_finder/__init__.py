"""generate Network Devices (Switch/Router) facts from its configuration outputs.
"""

# ------------------------------------------------------------------------------

from .generators.merger import device
from .generators.merger import DeviceDB
from .rearrange import rearrange_tables
from .generators import get_necessary_cmds, get_absolute_command

from .clean import CleanFacts



__all__ = [ 
	'device', 'DeviceDB',
	'CleanFacts',
	'rearrange_tables',
	'get_necessary_cmds', 'get_absolute_command',
	]

__ver__ = "0.1.0"