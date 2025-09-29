# brandizpyes.logging

## Functions

| [`logger_config`](#brandizpyes.logging.logger_config)(→ logging.Logger | None)   | Configures the Python logging module with a YAML configuration file.   |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------|

## Module Contents

### brandizpyes.logging.logger_config(logger_name=None, cfg_path=None, disable_existing_loggers=False) → logging.Logger | None

Configures the Python logging module with a YAML configuration file.

The file name is picked, in order: from cfg_path if provided, from the environment variable
PYES_LOG_CONF, from <current directory>/logging.yaml.

This should be called at the begin of a main program and BEFORE any use of the logging module.
Multiple calls of this method are idempotent, ie, the Python logging module configures itself
once only (and only before sending in logging messages).

An example of logging config file is included in the package test files.

If logger_name is provided, the function returns logging.getLogger ( logger_name ) as a facility
to avoid the need to import logging too, when you already import this. Beware that you load a configuration
one only in your application (so, don’t use this method in modules just to get a logger).

param disable_existing_loggers is false by default, this is the best way to not interfere with modules instantiating
their own module logger, usually before you call this function on top of your application (but usually after
all the imports). By default, the Python logging library has this option set to true and that typically causes
all the module loggers to be disabled after the configuration loading. See [https://docs.python.org/3/library/logging.config.html](https://docs.python.org/3/library/logging.config.html)
