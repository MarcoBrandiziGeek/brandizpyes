from brandizpyes.logging import logger_config
import logging
import os, io, sys
import tempfile


	
def test_basics ():

	old_stderr = sys.stderr
	std_err = sys.stderr = io.StringIO()

	os.environ [ "PYES_LOG_CONF_PATH" ] = os.path.dirname ( __file__ ) + "/logging-explicitly-loaded.yml"

	# This config has a call to get the OS-dependent temp dir, so we need the unsafe loader
	logger_config ( use_unsafe_loader = True ) 
	
	log_file_path = os.path.join ( tempfile.gettempdir(), "brandiz-pyes.log" )
	
	log = logging.getLogger ( __name__ )
			
	info_msg = "Hi, this is an info message"
	log.info ( info_msg )
	
	err_msg = "Hi, this is an error message"
	log.error ( err_msg )

	debug_msg = "Hi, this is a debug message"
	log.debug ( debug_msg )

	std_err_str = std_err.getvalue()
	sys.stderr = old_stderr
	
	print ( "Captured output: " )
	print ( std_err_str )

	assert err_msg in std_err_str, "Error message not logged!"
	assert info_msg in std_err_str, "Info message not logged!"
	assert debug_msg not in std_err_str, "Debug message should not be logged in the console!"

	print ( "Loading the log file" )
	with open ( log_file_path ) as flog:
		log_file_str = flog.read()
		
	assert err_msg in log_file_str, "Error message not logged in the file!"
	assert info_msg in log_file_str, "Info message not logged in the file!"
	assert debug_msg in log_file_str, "Debug message not logged in the file!"


def test_default ():
	old_stderr = sys.stderr
	std_err = sys.stderr = io.StringIO()
	
	if "PYES_LOG_CONF_PATH" in os.environ: del os.environ [ "PYES_LOG_CONF_PATH" ]
	
	log = logger_config ( __name__ )
			
	info_msg = "Hi, this is an info message"
	log.info ( info_msg )
	
	err_msg = "Hi, this is an error message"
	log.error ( err_msg )

	debug_msg = "Hi, this is a debug message"
	log.debug ( debug_msg )


	std_err_str = std_err.getvalue()
	sys.stderr = old_stderr

	assert err_msg in std_err_str, "Error message not logged by the default config!"
	assert info_msg in std_err_str, "Info message not logged by the default config!"
	assert debug_msg not in std_err_str, "Debug message should not be logged by the default config!"


def test_common_name ():
	# cwd to myself
	os.chdir ( os.path.dirname ( __file__ ) )

	old_stderr = sys.stderr
	std_err = sys.stderr = io.StringIO()
	
	if "PYES_LOG_CONF_PATH" in os.environ: del os.environ [ "PYES_LOG_CONF_PATH" ]

	# So, it should get the logging-test.yml that sits alongside this file 
	log = logger_config ( __name__ )

	warn_msg = "Hi, this is a warning message"
	log.warning ( warn_msg )

	err_msg = "Hi, this is an error message"
	log.error ( err_msg )

	std_err_str = std_err.getvalue()
	sys.stderr = old_stderr

	assert err_msg in std_err_str, "Error message not logged by the common name logger!"
	assert warn_msg not in std_err_str, "Warning message should not be logged by the common name logger!"
