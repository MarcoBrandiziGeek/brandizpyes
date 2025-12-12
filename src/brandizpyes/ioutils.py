from io import StringIO
from typing import Callable, Optional, TextIO


def dump_output ( 
	writer: Callable [[TextIO], Optional[str]],
	out_path_or_io: Optional[str|TextIO] = None,
	mode = "w",
	**open_opts
) -> Optional[str]:
	"""
	Utility to quickly deal with a writer that writes on a file-like handle.

	Args:
		- writer: A function that takes a file-like object as its only argument and writes to it.

		- out_path: If this is a string, the function will open a file against the given path and
		will pass the corresponding file handle to the `writer` function. 
		Else, if it's a file-like object, it will be passed as-is to the `writer` function.
		If it's null, a :class:`StringIO` buffer will be used and its content returned as a string.

		- mode: The mode to open the file if `out_path` is a string, ie, the argument is passed to :fun:`open()`.
		
		- open_opts: Additional options passed to :fun:`open()`.

	Returns:
		str | None: If `out_path` is None, the function returns the content written to a StringIO.
		
	"""
	if out_path_or_io is None:
		output = StringIO()
		writer ( output )
		return output.getvalue()

	if isinstance ( out_path_or_io, str ):
		with open ( out_path_or_io, mode, **open_opts ) as fh:
			writer ( fh )
		return None
		
	# Else, assume it's a file-like object and pass it down
	writer ( out_path_or_io )
	return None
