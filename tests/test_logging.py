from typing import TextIO
from brandizpyes.logging import logger_config
import logging
import os, io, sys
import tempfile
import pytest


@pytest.mark.parametrize ( "source_type", [ "PATH", "ENV_VAR" ] )
def test_explicitly_loaded_config ( source_type: str ):
	"""
	Tests the loading of a logging configuration from either a path or a path set in a conventional
	environment variable.

	These two cases are parametrized in a single test, since they use the same file and verify
	the same logging behaviour.
	"""

	old_stderr = sys.stderr
	std_err_io = sys.stderr = io.StringIO()

	log = None

	if source_type == "PATH":
		# This test config has a call to get the OS-dependent temp dir, so we need the unsafe YAML loader
		# to enable that.
		#
		logger_config ( 
			cfg_path = os.path.dirname ( __file__ ) + "/logging-explicitly-loaded.yml",
			use_unsafe_loader = True 
		) 

		log = logging.getLogger ( __name__ )

	elif source_type == "ENV_VAR":
	  # Your app can set the logger config via this env var
		os.environ [ "PYES_LOG_CONF_PATH" ] = os.path.dirname ( __file__ ) + "/logging-explicitly-loaded.yml"

		# logger_config() can be used this way too. Typically, your app will call it upon start
		# and then its components/modules will use the standard Python logging module as usual.
		#
		log = logger_config ( __name__, use_unsafe_loader = True )

	else:
		raise ValueError ( f"Invalid source_type '{source_type}' for test_explicitly_loaded_config()" )

	# The same as the one in the config file
	log_file_path = os.path.join ( tempfile.gettempdir(), "brandiz-pyes.log" )

	info_msg = "Hi, this is an info message"
	log.info ( info_msg )
	
	err_msg = "Hi, this is an error message"
	log.error ( err_msg )

	debug_msg = "Hi, this is a debug message"
	log.debug ( debug_msg )

	std_err_str = std_err_io.getvalue()
	sys.stderr = old_stderr
	
	print ( "Captured output: " )
	print ( std_err_str )

	assert err_msg in std_err_str, "Error message not logged!"
	assert info_msg in std_err_str, "Info message not logged!"
	assert debug_msg not in std_err_str, "Debug message should not be logged in the console!"

	print ( "Verifying the log file" )
	with open ( log_file_path ) as flog:
		log_file_str = flog.read()
		
	assert err_msg in log_file_str, "Error message not logged in the file!"
	assert info_msg in log_file_str, "Info message not logged in the file!"
	assert debug_msg in log_file_str, "Debug message not logged in the file!"


def test_default_config ():
	"""
	No env var, no config file in the current dir, takes the package-included default config.
	"""

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


def test_config_from_common_path ():
	"""
	Chdir to this test file dir, so that it picks up logging-test.yml
	"""
	
	os.chdir ( os.path.dirname ( __file__ ) ) # myself

	old_stderr = sys.stderr
	std_err = sys.stderr = io.StringIO()
	
	if "PYES_LOG_CONF_PATH" in os.environ: del os.environ [ "PYES_LOG_CONF_PATH" ]

	log = logger_config ( __name__ )

	warn_msg = "Hi, this is a warning message"
	log.warning ( warn_msg )

	err_msg = "Hi, this is an error message"
	log.error ( err_msg )

	std_err_str = std_err.getvalue()
	sys.stderr = old_stderr

	assert err_msg in std_err_str, "Error message not logged by the common name logger!"
	assert warn_msg not in std_err_str, "Warning message should not be logged by the common name logger!"
