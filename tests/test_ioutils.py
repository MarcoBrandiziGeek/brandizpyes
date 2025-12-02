from io import StringIO
import os
import unittest
from contextlib import redirect_stdout
import tempfile

from assertpy import assert_that

from brandizpyes.ioutils import dump_output

def test_dump_output_to_file ():
	# Create a temp file, using the system's temp folder
	test_content = "Hello, file!\n"
	output_path = os.path.join ( tempfile.gettempdir (), 'ketl.ioutils.testdumpout.txt' )

	if os.path.exists ( output_path ):
		os.remove ( output_path )

	dump_output ( lambda fh: fh.write ( test_content ), output_path )
	
	with open ( output_path, 'r' ) as fh:
		content = fh.read()

	assert_that( content, "dump_output() to file succeeded" ).is_equal_to( test_content )

def test_dump_output_to_string ():
	test_content = "Hello, StringIO!\n"
	content = dump_output ( lambda fh: fh.write ( test_content ) )
	assert_that( content, "dump_output() to StringIO succeeded" ).is_equal_to( test_content )

def test_dump_output_to_stdout ():
	test_content = "Hello, stdout!\n"

	with redirect_stdout(StringIO()) as buffer:
		dump_output ( lambda fh: fh.write ( test_content ), buffer )
	
	content = buffer.getvalue ()
	assert_that( content, "dump_output() to stdout succeeded" ).is_equal_to( test_content )

