import io
import logging
import logging.config
import os
from sys import stderr
from typing import Callable

import yaml

from brandizpyes.threading import ReadWriteLock, FakeReadWriteLock

# TODO: support the rich library components, to get coloured output
# see https://chatgpt.com/share/68de70b6-2904-800d-a57a-54ede673f531
#


def logger_config(logger_name: str = None,
                  cfg_path: str = None,
                  disable_existing_loggers: bool = False,
                  use_unsafe_loader: bool = False) -> logging.Logger | None:
	"""
	Configures the Python logging module with a YAML configuration file.
	
	The file name is picked, in order: from cfg_path if provided, from the environment variable 
	PYES_LOG_CONF, from <current directory>/logging-test.yml or <current directory>/logging.yml.
	If none of these files exists, a [default configuration file](logging-default.yml) 
	included in this package is used.

	This should be called at the begin of an application and BEFORE any use of the logging module.
	Multiple calls of this method are idempotent, ie, the Python logging module configures itself
	once only (and only before sending in logging messages).
	
	An example of logging config file is included in the package test files.
	
	If logger_name is provided, the function returns logging.getLogger ( logger_name ) as a facility
	to avoid the need to import logging too, when you already import this. Beware that you load a configuration
	one only in your application (so, don't use this method in modules just to get a logger). 
	
	:param disable_existing_loggers: is false by default, this is the best way to not interfere with modules instantiating
	their own module logger, usually before you call this function on top of your application (but usually after 
	all the imports). By default, the Python logging library has this option set to true and that typically causes
	all the module loggers to be disabled after the configuration loading. See https://docs.python.org/3/library/logging.config.html

	:param use_unsafe_loader: if true, uses yaml.UnsafeLoader to load the configuration file. 
	This is useful when you want to do things like calling functions in the configuration file 
	(see logging-explicitly-loaded.yml in the tests). However, it's False by default, since this behaviour is
	unsafe (see Python documentation).
	"""

	if not cfg_path:
		for probed_path in (os.getenv("PYES_LOG_CONF_PATH", "logging-test.yml"), "logging.yml"):
			cfg_path = probed_path
			if os.path.isfile(probed_path): break

	if not os.path.isfile(cfg_path):
		print(
		    f"*** Logger config file '{cfg_path}' not found, use the OS variable PYES_LOG_CONF_PATH to point to a logging configuration.",
		    file=stderr)
		print("The logger will use a default configuration ", file=stderr)
		cfg_path = os.path.abspath(os.path.dirname(__file__) + "/logging-default.yml")

	loader = yaml.UnsafeLoader if use_unsafe_loader else yaml.FullLoader

	with open(cfg_path) as flog:
		cfg = yaml.load(flog, Loader=loader)
		# As per documentation, if not reset, this disables loggers in the modules, which usually are
		# loaded during 'import', before calling this function
		cfg["disable_existing_loggers"] = disable_existing_loggers
		logging.config.dictConfig(cfg)
	log = logging.getLogger(__name__)
	log.info("Logger configuration loaded from '%s'" % cfg_path)

	if logger_name: return logging.getLogger(logger_name)


class ProgressLogger:
	"""
	A helper class to log progress of a long-running process.

	Translated from [`jutils`][10] [`ProgressLogger`][20]

	[10]: https://github.com/marco-brandizi/jutils
	[20]: https://github.com/marco-brandizi/jutils/blob/master/src/main/java/uk/ac/ebi/utils/runcontrol/ProgressLogger.java
	"""

	progress_resolution: int = 1000
	"""
	The resolution of progress updates, ie, how many items
	should be processed before a new log message is generated
	"""

	log_message_template: str = "%d items processed"
	"""What's reported when a log event is trigged by a progress update and based on `progress_resolution`."""
	
	logging_level: int = logging.INFO
	"""
	The logging level to use for progress updates.
	"""

	progress_report_action: Callable[[int, int], None] = None
	"""
	A callback to be called when a progress update is triggered by `progress_resolution`.
	The callback receives the old and new progress values as arguments. By default, it logs 
	a message based on `log_message_template` and using the logger passed to `__init__` with 
	`logging_level` priority.
	"""

	def __init__(
		self,
		logger: logging.Logger,
		progress_resolution: int | None = None,
		log_message_template: str | None = None
	):
		self.logger = logger
		if progress_resolution is not None:
			self.progress_resolution = progress_resolution
		if log_message_template is not None:
			self.log_message_template = log_message_template

		self.progress_report_action = \
			lambda old, new: self.logger.log ( self.logging_level, self.log_message_template % new )
		self.set_is_thread_safe ( True )

		self._progress: int = 0

	@property
	def progress(self) -> int:
		"""
		Read-only property for progress value.
		"""
		return self._progress

	def reset ( self ):
		"""
		Resets the progress to 0.
		"""
		self.update ( 0 )

	def update ( self, new_progress: int ):
		"""
		Updates the current progress and possibly generates a new log message, according to `progress_resolution`.
	 	The new progress should be greater than the existing one, except for the value 0, which resets the logger 
		for a new process. 
	 	"""
		old_progress = self._progress
		self._lock.acquire_write ()
		try:
			self._progress = new_progress
		finally:
			self._lock.release_write ()
		if new_progress == 0: return # don't report progress when resetting
		self._progress_report ( old_progress, new_progress )

	def update_with_increment ( self, increment: int = 1 ):
		"""
		Same as `update`, but with incrementation of the existing progress.
		"""
		self._lock.acquire_write ()
		try:
			self.update ( self._progress + increment )
		finally:
			self._lock.release_write ()

	def _progress_report ( self, old_progress: int, new_progress: int ):
		"""
		Invoked by `update`, decides whether to report the progress, according to `progress_resolution`, 
		and possibly calls the `progress_report_action` callback.
		"""
		self._lock.acquire_read ()
		try:
			old_check_pt = int ( old_progress / self.progress_resolution )
			new_check_pt = int ( new_progress / self.progress_resolution )
			if new_check_pt - old_check_pt == 0: return
		finally:
			self._lock.release_read ()
		self.progress_report_action ( old_progress, new_progress )

	def set_is_thread_safe ( self, is_thread_safe: bool = True ):
		"""
	 	Tells us that progress updates will be thread-safe, so that we can spare some overhead for
		synchronising concurrent updates to the progress value.
		
		Default is True
	   
	 	**WARNING**: do I need to tell you?
		"""		
		self._lock = FakeReadWriteLock() if is_thread_safe else ReadWriteLock()

	def append_progress_report_action ( self, progress_report_action: Callable[[int, int], None] ):
		"""
		Appends a new progress report action to the existing one.

		This can be useful when you want to add your additional stuff to the default logging.
		See the `progress_report_action` property.		
		"""
		current_action = self.progress_report_action
		if current_action is None:
			self.progress_report_action = progress_report_action
			return

		def chained_action(old, new):
			current_action (old, new)
			progress_report_action ( old, new )

		self.progress_report_action = chained_action


class PercentProgressLogger ( ProgressLogger ):
	"""
	A `ProgressLogger` that reports progress in percentage, instead of absolute values.

	Translated from [jutils][10] [PercentProgressLogger][20]

	[10]: https://github.com/marco-brandizi/jutils
	[20]: https://github.com/marco-brandizi/jutils/blob/master/src/main/java/uk/ac/ebi/utils/runcontrol/PercentProgressLogger.java
	"""

	max_progress: int = 100
	"""
	The maximum progress value, used to calculate the percentage.
	"""

	progress_resolution: int = 10
	log_message_template: str = "%d%% completed"


	def __init__(
		self,
		logger: logging.Logger,
		max_progress: int | None = None,
		progress_resolution: int | None = None,
		log_message_template: str | None = None
	):
		super().__init__ ( logger, progress_resolution, log_message_template )
		if max_progress is not None:
			self.max_progress = max_progress

	def _progress_report ( self, old_progress: int, new_progress: int ):
		"""
		Internally, it works by always converting the absolutes to percentages.
		"""
		old_percent = round ( old_progress * 100 / self.max_progress )
		new_percent = round ( new_progress * 100 / self.max_progress )
		super()._progress_report ( old_percent, new_percent )

	@property
	def percent_progress(self) -> float:
		"""
		Read-only property for percentage progress value.
		"""
		return self._progress * 100.0 / self.max_progress
	