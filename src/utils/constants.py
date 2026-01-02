'''
Constants for all of EOM-Insights
'''

import os
import utils.io_utils as io_utils

# Logging
DEFAULT_LOG_LEVEL = 'WARNING'

LOG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..','logs')
io_utils.ensure_directory_exists(LOG_PATH)
DEBUG_LOG_FORMAT = '{}.log' # Filename will be formatted logger name
ERROR_LOG_FILENAME = 'error.log'

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' # Used for warn, error & debug

#Debug
DEBUG_ENABLED = False

# Category
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'data')
io_utils.ensure_directory_exists(DATA_PATH)

CATEGORY_PATH = os.path.join(DATA_PATH, 'categories')
io_utils.ensure_directory_exists(CATEGORY_PATH)

CATEGORY_FILE_FORMAT = '{}.json'

