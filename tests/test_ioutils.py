import os
import sys
import tempfile

from assertpy import assert_that

from brandizpyes.ioutils import dump_output


def test_dump_output_to_file ():
	test_content = "Hello, file!\n"
	output_path = os.path.join ( tempfile.gettempdir (), 'ketl.ioutils.testdumpout.txt' )

	if os.path.exists ( output_path ): os.remove ( output_path )

	# Dump to this path
	dump_output ( lambda fh: fh.write ( test_content ), output_path )
	
	with open ( output_path, 'r' ) as fh:
		content = fh.read()

	assert_that( content, "dump_output() to file succeeded" ).is_equal_to( test_content )

def test_dump_output_to_string ():
	test_content = "Hello, StringIO!\n"

	# No other parameter, dumps to a StringIO and returns its content
	content = dump_output ( lambda fh: fh.write ( test_content ) )
	
	assert_that( content, "dump_output() to StringIO succeeded" )\
		.is_equal_to( test_content )

def test_dump_output_to_stdout ( capsys ):
	test_content = "Hello, stdout!\n"

	# Dumps to the file-like object sys.stdout
	dump_output ( lambda fh: fh.write ( test_content ), sys.stdout )
	content = capsys.readouterr().out

	assert_that( content, "dump_output() to stdout succeeded" )\
		.is_equal_to( test_content )
