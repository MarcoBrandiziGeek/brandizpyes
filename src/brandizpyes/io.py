from io import StringIO
from pathlib import Path
import sys
from typing import Any, Callable, Optional, TextIO


def dump_output ( 
	writer: Callable[[TextIO], None],
	out_path_or_io: str|TextIO|None = None,
	mode: str = "w",
	**open_opts
) -> str|None:
	"""
	Utility to quickly deal with a writer that writes on a file-like handle.

	Args:
		- writer: A function that takes a file-like object as its only argument and writes to it.

		- out_path_or_io: If this is a string, the function will open a file against the given path and
		will pass the corresponding file handle to the `writer` function. 
		Else, if it's a file-like object, it will be passed as-is to the `writer` function.
		If it's null, a :class:`StringIO` buffer will be used and its content returned as a string.

		- mode: The mode to open the file if `out_path_or_io` is a string, ie, the argument is passed to :fun:`open()`.
		
		- open_opts: Additional options passed to :fun:`open()`.

	Returns:
		str | None: If `out_path_or_io` is None, the function returns the content written to a StringIO.
		
	"""
	if out_path_or_io is None:
		output = StringIO ()
		writer ( output )
		return output.getvalue()

	if isinstance ( out_path_or_io, str ):
		with open ( out_path_or_io, mode, **open_opts ) as fh:
			writer ( fh )
		return None

	if hasattr ( out_path_or_io, "write" ) and callable ( out_path_or_io.write ):
		writer ( out_path_or_io )
		return None		
	
	raise ValueError ( f"dump_output(), {type ( out_path_or_io )} is invalid for out_path_or_io" )


def reader_helper (
	reader: Callable[[TextIO], Any|None],
	input_source: str|Path|TextIO|None = None,
	mode: str = "r", 
	**open_opts
) -> Any|None:
	"""
	Utility to quickly deal with an input that can be either a file path, a file-like object, or a string
	to read from.

	Args:
		- reader: A function that takes a file-like object as its only argument and reads from it, possibly returning
		some result.
		- input_source: If this is a `Path`, the function will open a file against the given path and
		will call `reader` with it. It will call `reader` if this argument is a file-like object, and in
		case of a string, it will create a `StringIO` from it and pass the handler to the reader.
		Finally, if it's null, it will pass the stdin to the reader.
		- mode: The mode to open the file if `input_source` is a `Path`, ie, the argument is passed to :fun:`open()`.		
		- open_opts: Additional options passed to :fun:`open()`.

	Returns:
		Whatever `reader` returns, including None.
	"""
	if input_source is None:
		return reader ( sys.stdin )
	if isinstance ( input_source, str ):
		return reader ( StringIO ( input_source ) )
	if isinstance ( input_source, Path ):
		with open ( input_source, mode, **open_opts ) as fh:
			return reader ( fh )
	if hasattr ( input_source, "read" ) and callable ( input_source.read ):
		return reader ( input_source )
	
	raise ValueError ( f"reader_helper(), {type( input_source )} is invalid for input_source" )
