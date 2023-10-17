###
# Singleton logger that removes issues with the logger being loaded multiple times and duplicating log entries
# Logs to stdout unless the ENV variable LOG_DESTINATION is present.
# Currently LOG_DESTINATION only support PAPERTRAIL
###
import os, sys
import logging
import socket

from cc_py_commons.config.env import env_name, app_config

PAPERTRAIL = 'PAPERTRAIL'

class ContextFilter(logging.Filter):
	hostname = socket.gethostname()

	def filter(self, record):
		record.hostname = ContextFilter.hostname
		return True

class SingletonLogger:
	_instance = None

	@staticmethod
	def getInstance():
		if SingletonLogger._instance == None:
			SingletonLogger()

		return SingletonLogger._instance

	def __init__(self):
		if SingletonLogger._instance != None:
			raise Exception("This class is a singleton!")
		else:
			SingletonLogger._instance = self._config_logger()

	def _config_logger(self):
		logger = logging.getLogger(app_config.LOG_APP_NAME)
		logger.setLevel(app_config.LOG_LEVEL)

		contextFilter = ContextFilter()
		logger.addFilter(contextFilter)
		formatter = logging.Formatter('{}: %(levelname)s %(message)s'.format(app_config.LOG_APP_NAME),
														datefmt='%Y-%m-%d %I:%M:%S %p')

		log_destination = os.environ.get('LOG_DESTINATION')
			
		if log_destination == PAPERTRAIL:
			syslog = logging.handlers.SysLogHandler(address=('logs3.papertrailapp.com', 10024))
		else:
			syslog = logging.StreamHandler(sys.stdout)

		syslog.setFormatter(formatter)
		
		if not logger.handlers:
			logger.addHandler(syslog)
			
		return logger

# Usage
logger = SingletonLogger.getInstance()
