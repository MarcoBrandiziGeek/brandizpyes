import os

from brandizpyes.logging import logger_config

"""
Pytest configuration file, which the framework picks up at startup.

[Details here](https://docs.pytest.org/en/stable/reference/fixtures.html)

"""
def pytest_configure ( config ):
	"""
	As per their docs, this is picked up by pytest at startup.
	"""

	# We can't use the usual logging-test.yml inside our own tests, since this is already used to
	# test the brandizpyes.logging module.
	#
	cfg_path = os.path.dirname ( __file__ ) + "/resources/logging-brandizpyes-test.yml"
	logger_config ( __name__, cfg_path )

