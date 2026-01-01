'''
Constants for all of EOM-Insights
'''

import os
import platformdirs

# Logging
DEFAULT_LOG_LEVEL = 'WARNING'

LOG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..','logs')
DEBUG_LOG_FORMAT = '{}.log' # Filename will be formatted logger name
ERROR_LOG_FILENAME = 'error.log'

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEBUG_ENABLED = False

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper