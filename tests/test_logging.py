from brandizpyes.logging import logger_config
import logging
import os, io, sys


	
def test_basics ():
	#import debugpy
	#debugpy.breakpoint()

	old_stderr = sys.stderr
	err = sys.stderr = io.StringIO()
	
	os.environ [ "PYES_LOG_CONF_PATH" ] = os.path.dirname ( __file__ ) + "/logging-test.yml"
	logger_config ()
	
	log = logging.getLogger ( __name__ )
			
	info_msg = "Hi, this is an info message"
	log.info ( info_msg )
	
	err_msg = "Hi, this is an error message"
	log.error ( err_msg )

	err_str = err.getvalue()
	sys.stderr = old_stderr
	
	print ( "Captured output: " )
	print ( err_str )
	
	assert err_msg in err_str, "Error message not logged!"
	assert info_msg in err_str, "Info message not logged!"
