__doc__ = '''Networking Tool Set database functions
'''


__all__ = [
	# .convertdict
	'ConvDict',
	#databse
	"write_to_xl", "append_to_xl", "read_xl", "get_merged_DataFrame_of_file"
]


__version__ = "0.0.1"


from .convertdict import ConvDict
from .database import write_to_xl, append_to_xl, read_xl, get_merged_DataFrame_of_file


def version():
	return __version__