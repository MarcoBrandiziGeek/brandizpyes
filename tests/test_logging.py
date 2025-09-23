from brandizpyes.logging import logger_config

import os
import sys


"""
	There are issues with the already set loggers, keep it as last one.
"""	
class TestLogging ( unittest.TestCase ):
	
	def test_basics ( self ):
		
		old_stderr = sys.stderr
		err = sys.stderr = io.StringIO()
		
		os.environ [ "ETL_LOG_CONF" ] = os.path.dirname ( __file__ ) + "/logging.yaml"
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
		
		self.assertTrue ( err_msg in err_str, "Error message not logged!" )
		self.assertTrue ( info_msg in err_str, "Info message not logged!" )

		
if __name__ == '__main__':
	logger_config ()
	unittest.main()
