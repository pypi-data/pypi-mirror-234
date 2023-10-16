__doc__ = '''Networking Tool Set for Juniper devices
'''


__all__ = [
	# .juniper
	'Juniper', 'convert_to_set_from_captures',
	# Jset
	'JSet',
	]


__version__ = "0.0.1"


from .juniper import Juniper, convert_to_set_from_captures
from .jset import JSet


def version():
	return __version__