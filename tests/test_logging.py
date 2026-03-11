import io
import logging
import os
import sys
import tempfile

import pytest
from assertpy import assert_that

from brandizpyes.logging import PercentProgressLogger, ProgressLogger, logger_config


@pytest.mark.parametrize ( "source_type", [ "PATH", "ENV_VAR" ] )
def test_logger_config_explicitly_loaded_config ( source_type: str ):
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
			cfg_path = 
				os.path.dirname ( __file__ ) + "/resources/logging-explicitly-loaded.yml",
			use_unsafe_loader = True 
		)

		log = logging.getLogger ( __name__ )

	elif source_type == "ENV_VAR":
	  # Your app can set the logger config via this env var
		os.environ [ "PYES_LOG_CONF_PATH" ] = \
			os.path.dirname ( __file__ ) + "/resources/logging-explicitly-loaded.yml" 
		

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

	assert_that ( std_err_str, "Error message was logged" ).contains ( err_msg )
	assert_that ( std_err_str, "Info message was logged" ).contains ( info_msg )
	assert_that ( std_err_str, "Debug message was not logged in the console" ).does_not_contain ( debug_msg )

	print ( "Verifying the log file" )
	with open ( log_file_path ) as flog:
		log_file_str = flog.read ()
		
	assert_that ( log_file_str, "Error message was logged in the file" ).contains ( err_msg )
	assert_that ( log_file_str, "Info message was logged in the file" ).contains ( info_msg )
	assert_that ( log_file_str, "Debug message was logged in the file" ).contains ( debug_msg )


def test_logger_config_default_config ():
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

	assert_that ( std_err_str, "Error message was logged by the default config" ).contains ( err_msg )
	assert_that ( std_err_str, "Info message was logged by the default config" ).contains ( info_msg )
	assert_that ( std_err_str, "Debug message was not logged by the default config" ).does_not_contain ( debug_msg )


def test_logger_config_config_from_common_path ():
	"""
	Chdir to the test resources dir, so that it picks up logging-test.yml
	"""
	
	os.chdir ( os.path.dirname ( __file__ ) + "/resources" ) # myself

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

	assert_that ( std_err_str, "Error message was logged by the common name logger" ).contains ( err_msg )
	assert_that ( std_err_str, "Warning message was not logged by the common name logger" ).does_not_contain ( warn_msg )


@pytest.fixture ()
def reset_logger_config_fixture ():
	"""Reset the logger after the previous tests"""
	cfg_path = os.path.dirname ( __file__ ) + "/resources/logging-brandizpyes-test.yml"
	logger_config ( __name__, cfg_path )


@pytest.mark.parametrize (
	ids = lambda is_thread_safe: "single-thread" if is_thread_safe else "multi-thread",
	argnames = "is_thread_safe",
	argvalues = [ True, False ]
)
@pytest.mark.usefixtures ( "reset_logger_config_fixture" )
def test_progress_logger ( caplog, is_thread_safe: bool ):
	log = logging.getLogger ( __name__ )
	prog_logger = ProgressLogger ( log, progress_resolution = 100 )
	# when true, we make sure the internal locking works
	prog_logger.set_is_thread_safe ( is_thread_safe ) 

	prog_logger.update ( 100 )
	assert_that ( prog_logger.progress, "Progress was updated to 100" ).is_equal_to ( 100 )
	
	prog_logger.update_with_increment ()
	assert_that ( prog_logger.progress, "Progress was updated to 101" ).is_equal_to ( 101 )
	
	prog_logger.update_with_increment ( 100 )
	assert_that ( prog_logger.progress, "Progress was updated to 201" ).is_equal_to ( 201 )
	
	prog_logger.update_with_increment ( 50 )
	assert_that ( prog_logger.progress, "Progress was updated to 251" ).is_equal_to ( 251 )

	for i in range ( 1, 50 ):
		prog_logger.update_with_increment ()
	assert_that ( prog_logger.progress, "Progress was updated to 300" ).is_equal_to ( 300 )

	assert_that ( caplog.messages, "100 was logged" )\
		.contains ( "100 items processed" )\
		.described_as ( "101 isn't reported" ).does_not_contain ( "101 items processed" )\
		.described_as ( "201 is reported" ).contains ( "201 items processed" )\
		.described_as ( "251 isn't reported" ).does_not_contain ( "251 items processed" )\
		.described_as ( "270 isn't reported" ).does_not_contain ( "270 items processed" )\
		.described_as ( "300 is reported" ).contains ( "300 items processed" )


@pytest.mark.usefixtures ( "reset_logger_config_fixture" )
def test_percent_progress_logger ( caplog ):
	log = logging.getLogger ( __name__ )
	prog_logger = PercentProgressLogger ( 
		log, max_progress = 1000, log_message_template = "%.2f%% of items processed"
	)
	prog_logger.update ( 100 )
	assert_that ( prog_logger.progress, "Progress was updated to 100" ).is_equal_to ( 100 )
	assert_that ( prog_logger.percent_progress, "Percent progress was updated to 10%" ).is_equal_to ( 10.0 )

	prog_logger.update_with_increment ( 50 )
	assert_that ( prog_logger.progress, "Progress was updated to 150" ).is_equal_to ( 150 )
	assert_that ( prog_logger.percent_progress, "Percent progress was updated to 15%" ).is_equal_to ( 15.0 )

	prog_logger.update_with_increment ( 300 )
	assert_that ( prog_logger.progress, "Progress was updated to 450" ).is_equal_to ( 450 )
	assert_that ( prog_logger.percent_progress, "Percent progress was updated to 45%" ).is_equal_to ( 45.0 )

	prog_logger.update_with_increment ( 5 )
	assert_that ( prog_logger.progress, "Progress was updated to 455" ).is_equal_to ( 455 )
	assert_that ( prog_logger.percent_progress, "Percent progress was updated to 45.5%" ).is_equal_to ( 45.5 )
	
	prog_logger.update_with_increment ( 545 )
	assert_that ( prog_logger.progress, "Progress was updated to 1000" ).is_equal_to ( 1000 )
	assert_that ( prog_logger.percent_progress, "Percent progress was updated to 100%" ).is_equal_to ( 100.0 )

	assert_that ( caplog.messages, "10% was logged" )\
	.contains ( "10.00% of items processed" )\
	.described_as ( "15% isn't reported" ).does_not_contain ( "15.00% of items processed" )\
	.described_as ( "45% was logged" ).contains ( "45.00% of items processed" )\
	.described_as ( "100% was logged" ).contains ( "100.00% of items processed" )


@pytest.mark.usefixtures ( "reset_logger_config_fixture" )
def test_percent_progress_logger_custom_report_action ( caplog ):
	log = logging.getLogger ( __name__ )

	"""
			PercentProgressLogger progTracker = new PercentProgressLogger ( "{}% of items processed", 1000 );
		progTracker.appendProgressReportAction ( 
			(oldp, newp) -> log.info ( "custom progress report action: {}%", newp )
		);
		progTracker.update ( 100 );

		System.setOut ( outBkp );  // restore the original output
		
		String outStr = outBuf.toString ();
		
		log.info ( "Output from the progress logger:\n\n-------------------\n{}-------------------\n", outStr );
		
		Assert.assertTrue ( "10% not reported!", outStr.contains ( "10% of items processed" ) );
		Assert.assertTrue ( "custom 10% not reported!", outStr.contains ( "custom progress report action: 10%" ) );
	"""
	prog_logger = PercentProgressLogger ( log, max_progress = 1000, log_message_template = "%.2f%% of items processed" )
	prog_logger.append_progress_report_action ( lambda oldp, newp: log.info ( "custom progress report action: %.2f%%", newp ) )
	prog_logger.update ( 100 )

	assert_that ( caplog.messages, "10% was logged by the default report action" )\
	.contains ( "10.00% of items processed" )\
	.described_as ( "10% was logged by the custom report action" )\
		.contains ( "custom progress report action: 10.00%" )


