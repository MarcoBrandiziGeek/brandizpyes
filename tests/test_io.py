from io import StringIO
import os
from pathlib import Path
import sys
import tempfile

from assertpy import assert_that
import pytest

from brandizpyes.io import async_reader_helper, dump_output, reader_helper


class TestDumpOutput:

	def test_to_file ( self ):
		test_content = "Hello, file!\n"
		output_path = os.path.join ( tempfile.gettempdir (), 'ketl.ioutils.testdumpout.txt' )

		if os.path.exists ( output_path ): os.remove ( output_path )

		# Dump to this path
		dump_output ( lambda fh: fh.write ( test_content ), output_path )
		
		with open ( output_path, 'r' ) as fh:
			content = fh.read()

		assert_that( content, "dump_output() to file succeeded" ).is_equal_to( test_content )


	def test_to_string ( self ):
		test_content = "Hello, StringIO!\n"

		# No other parameter, dumps to a StringIO and returns its content
		content = dump_output ( lambda fh: fh.write ( test_content ) )
		
		assert_that( content, "dump_output() to StringIO succeeded" )\
			.is_equal_to( test_content )


	def test_to_stdout ( self, capsys ):
		test_content = "Hello, stdout!\n"

		# Dumps to the file-like object sys.stdout
		dump_output ( lambda fh: fh.write ( test_content ), sys.stdout )
		# capsys is a pytest helper, see their docs
		content = capsys.readouterr().out

		assert_that( content, "dump_output() to stdout succeeded" )\
			.is_equal_to( test_content )
		
	def test_to_iterable ( self ):
		test_content = [ "Hello, iterable!\n", 1, 2, 3 ]

		# Dumps to an iterable, in this case a list, and returns whatever the writer returns
		iter_writer = lambda items: "".join ( str(item) for item in items )
		content = dump_output ( iter_writer, test_content )

		assert_that( content, "dump_output() to iterable succeeded" )\
			.is_equal_to( iter_writer ( test_content ) )


class TestReaderHelper:
	def test_from_string ( self ):
		test_content = "Hello, StringIO!\n"
		content = reader_helper ( lambda fh: fh.read (), test_content )
		assert_that ( content, "reader_helper() from string succeeded" )\
			.is_equal_to ( test_content )

	def test_from_file ( self ):
		test_content = "Hello, file!\n"
		# First write it
		input_path = Path ( os.path.join ( tempfile.gettempdir (), 'ketl.ioutils.testinput.txt' ) )
		if input_path.exists (): input_path.unlink ()
		with open ( input_path, 'w' ) as fh:
			fh.write ( test_content )

		# And now use it to test
		content = reader_helper ( lambda fh: fh.read (), input_path )
		assert_that ( content, "reader_helper() from file succeeded" )\
			.is_equal_to ( test_content )
	
	def test_from_stdin ( self, capsys ):
		test_content = "Hello, stdin!\n"
		sys.stdin = StringIO ( test_content )

		content = reader_helper ( lambda fh: fh.read () )
		assert_that ( content, "reader_helper() from stdin succeeded" )\
			.is_equal_to ( test_content )
		
	def test_from_iterable ( self ):
		test_content = [ "Hello, iterable!\n", 1, 2, 3 ]
		iter_reader = lambda items: "".join ( str(item) for item in items )
		content = reader_helper ( iter_reader, test_content )
		assert_that ( content, "reader_helper() from iterable succeeded" )\
			.is_equal_to ( iter_reader ( test_content ) )


class TestAsyncReaderHelper:
	@classmethod
	async def async_file_read ( cls, fh ):
		return fh.read()
	
	@pytest.mark.asyncio
	async def test_from_string ( self ):
		test_content = "Hello, StringIO!\n"
		content = await async_reader_helper ( self.async_file_read, test_content )
		assert_that ( content, "async_reader_helper() from string succeeded" )\
			.is_equal_to ( test_content )

	@pytest.mark.asyncio
	async def test_from_file ( self ):
		test_content = "Hello, file!\n"
		# First write it. TODO: make it a fixture
		input_path = Path ( os.path.join ( tempfile.gettempdir (), 'ketl.ioutils.testinput.txt' ) )
		if input_path.exists (): input_path.unlink ()
		with open ( input_path, 'w' ) as fh:
			fh.write ( test_content )

		# And now use it to test
		content = await async_reader_helper ( self.async_file_read, input_path )
		assert_that ( content, "async_reader_helper() from file succeeded" )\
			.is_equal_to ( test_content )
	
	@pytest.mark.asyncio
	async def test_from_stdin ( self, capsys ):
		test_content = "Hello, stdin!\n"
		sys.stdin = StringIO ( test_content )

		content = await async_reader_helper ( self.async_file_read )
		assert_that ( content, "async_reader_helper() from stdin succeeded" )\
			.is_equal_to ( test_content )
		
	@pytest.mark.asyncio
	async def test_from_iterable ( self ):
		async def iter_reader ( items ):
			return "".join ( str(item) for item in items )
		
		test_content = [ "Hello, iterable!\n", 1, 2, 3 ]
		content = await async_reader_helper ( iter_reader, test_content )
		assert_that ( content, "async_reader_helper() from iterable succeeded" )\
			.is_equal_to ( "".join ( str(item) for item in test_content ) )
