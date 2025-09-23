def logger_config ( logger_name = None, disable_existing_loggers = False ):
	"""
	Configures the Python logging module with a YAML configuration file.
	
	The file name is picked from KPY_LOG_CONF, or from <current directory>/logging.yaml
	This should be called at the begin of a main program and BEFORE any use of the logging module.
	Multiple calls of this method are idempotent, ie, the Python logging module configures itself
	once only (and only before sending in logging messages).
	
	An example of logging config file is included in ETL tools.
	
	If logger_name is provided, the function returns logging.getLogger ( logger_name ) as a facility
	to avoid the need to import logging too, when you already import this. Beware that you load a configuration
	one only in your application (so, don't use this method in modules just to get a logger). 
	
	param disable_existing_loggers is false by default, this is the best way to not interfere with modules instantiating
	their own module logger, usually before you call this function on top of your application (but usually after 
	all the imports). By default, the Python logging library has this otpion set to true and that typically causes
	all the module loggers to be disabled after the configuration loading. See https://docs.python.org/3/library/logging.config.html
	"""

	cfg_path = os.getenv ( "KPY_LOG_CONF_PATH", "logging.yaml" )
	if not os.path.isfile ( cfg_path ):
		print ( "*** Logger config file '%s' not found, use the OS variable KPY_LOG_CONF to point to a logging configuration." % cfg_path, file = stderr )
		print ( "The logger will use the default configuration ", file = stderr )
		return logging.getLogger ( logger_name ) if logger_name else None 

	with open ( cfg_path ) as flog:		
		cfg = yaml.load ( flog, Loader = yaml.FullLoader )
		# As per documentation, if not reset, this disables loggers in the modules, which usually are 
		# loaded during 'import', before calling this function
		cfg [ "disable_existing_loggers" ] = disable_existing_loggers
		logging.config.dictConfig ( cfg )
	log = logging.getLogger ( __name__ )
	log.info ( "Logger configuration loaded from '%s'" % cfg_path )

	if logger_name: return logging.getLogger ( logger_name )
	