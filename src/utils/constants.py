'''
Constants for all of EOM-Insights
'''

import os
import platformdirs

# Logging
DEFAULT_LOG_LEVEL = 'WARNING'

DEBUG_LOG_PATH = os.path.join('..', '..','logs')
DEBUG_LOG_FORMAT = '{}.log' # Filename will be formatted logger name

ERROR_LOG_PATH = platformdirs.user_log_dir(appname="EOM-Insight")
ERROR_LOG_FORMAT = '{}_error.log' # Filename will be formatted logger name