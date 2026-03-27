from csv import reader
from io import StringIO
from pathlib import Path
import sys
from typing import Any, Awaitable, Callable, Iterable, TextIO


def dump_output ( 
	writer: Callable[[TextIO|Iterable[Any]], Any|None],
	out_sink: str|TextIO|Iterable[Any]|None = None,
	mode: str = "w",
	**open_opts
) -> str|None:
	"""
	Utility to quickly deal with a writer that writes on a file-like handle or an iterable.

	Args:
		- writer: A function that takes a file-like object as its only argument and writes to it.

		- out_sink: If this is a string, the function will open a file against the given path and
		will pass the corresponding file handle to the `writer` function. 
		Else, if it's a file-like object, it will be passed as-is to the `writer` function.
		If it's an iterable, it will also pass it as-is to the writer, but it will return whatever
		the writer returns. If the sink is null, a :class:`StringIO` buffer will be used and its content 
		returned as a string.

		- mode: The mode to open the file if `out_sink` is a string, ie, the argument is passed to :fun:`open()`.
		
		- open_opts: Additional options passed to :fun:`open()`.

	Returns:
		str | None: If `out_sink` is None, the function returns the content written to a StringIO. 
		If `out_sink` is an iterable, it returns whatever the writer returns.
		
	We support this variety of input types to cover both production and test cases.	
	"""
	if out_sink is None:
		output = StringIO ()
		writer ( output )
		return output.getvalue()

	if isinstance ( out_sink, str ):
		with open ( out_sink, mode, **open_opts ) as fh:
			writer ( fh )
		return None

	if hasattr ( out_sink, "write" ) and callable ( out_sink.write ):
		writer ( out_sink )
		return None		
	
	if isinstance ( out_sink, Iterable ):
		return writer ( out_sink )
	
	raise ValueError ( f"dump_output(), {type ( out_sink )} is invalid for out_sink" )


def reader_helper (
	reader: Callable[[TextIO|Iterable[Any]], Any|None],
	input_source: str|Path|TextIO|Iterable[Any]|None = None,
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
		will call `reader` with it. It will call `reader` if this argument is a file-like object or an iterable, and
		in case of a string, it will create a `StringIO` from it and pass the handler to the reader.
		Finally, if it's null, it will pass the stdin to the reader.
		
		- mode: The mode to open the file if `input_source` is a `Path`, ie, the argument is passed to :fun:`open()`.		
		- open_opts: Additional options passed to :fun:`open()`.

	Returns:
		Whatever `reader` returns, including None.

	We support this variety of input types to cover both production and test cases.

	**WARNING**: If the reader is an async function, use :func:`async_reader_helper`, see its docstring for details.
	"""
	if input_source is None:
		return reader ( sys.stdin )
	if isinstance ( input_source, str ):
		return reader ( StringIO ( input_source ) )
	if isinstance ( input_source, Path ):
		with open ( input_source, mode, **open_opts ) as fh:
			return reader ( fh )
	if isinstance ( input_source, Iterable ) or \
		 hasattr ( input_source, "read" ) and callable ( input_source.read ):
		return reader ( input_source )
	
	raise ValueError ( f"reader_helper(), {type( input_source )} is invalid for input_source" )

async def async_reader_helper (
	reader: Callable[[TextIO|Iterable[Any]], Awaitable[Any|None]],
	input_source: str|Path|TextIO|Iterable[Any]|None = None,
	mode: str = "r", 
	**open_opts
) -> Any|None:
	"""
	Async version of :func:`brandizpyes.io.reader_helper`.

	This works the same as the synch counterpart, except the reader is a coroutine and this helper
	awaits its result before returning it.

	This **must** be the version to use in an async context (ie, the reader is async), else the 
	sync version will just return the reader as a coroutine and will quit before the reader has 
	done anything, which later results in an error, since a file handle or alike has been closed
	already by the helper.

	TODO: do we need `async_dump_output_helper()` too? 
	"""
	
	if input_source is None:
		return await reader ( sys.stdin )
	if isinstance ( input_source, str ):
		return await reader ( StringIO ( input_source ) )
	if isinstance ( input_source, Path ):
		with open ( input_source, mode, **open_opts ) as fh:
			return await reader ( fh )
	if isinstance ( input_source, Iterable ) or \
		 hasattr ( input_source, "read" ) and callable ( input_source.read ):
		return await reader ( input_source )
	
	raise ValueError ( f"async_reader_helper(), {type( input_source )} is invalid for input_source" )