import datetime
import logging
import os

from utils.decorators import run_once
import utils.constants as constants

_error_handler = None
_log_dir = None

'''Sets up the root logger for the application.'''
@run_once
def setup_root_logger(logLevel=constants.DEFAULT_LOG_LEVEL):

    if (constants.DEBUG_ENABLED):
        logLevel = 'DEBUG'
    
    if not os.path.exists(constants.LOG_PATH):
        os.makedirs(constants.LOG_PATH)
        
    # Log file name is based on date to make tracking easier
    formattedTime = datetime.datetime.now().strftime('%Y-%m-%d')
    fileNameFormat = f'general_{formattedTime}.log'
    localFilePath = os.path.join(constants.LOG_PATH, fileNameFormat)
        
    root = logging.getLogger()
    root.setLevel(logLevel)
    
    # Add a blank line in the log file to separate runs
    osFilePath = os.path.join(constants.LOG_PATH, fileNameFormat)
    if (os.path.exists(osFilePath) and os.path.getsize(osFilePath) > 0):
        bh = logging.FileHandler(localFilePath)
        bh.setLevel(logging.INFO)
        bh.setFormatter(logging.Formatter(''))
        root.addHandler(bh)
        root.info('')
        root.info('')
        root.removeHandler(bh)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler(localFilePath)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(constants.LOG_FORMAT)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    root.addHandler(ch)
    root.addHandler(fh)
    pass

def create_logger(name):
    if '.' in name:
        name = name.replace('.', '-')
    if '_' in name:
        name = name.replace('_', '')    
    
    logger = logging.getLogger(name)
    
    if (constants.DEBUG_ENABLED):
        debugFilePath = os.path.join(constants.LOG_PATH, constants.DEBUG_LOG_FORMAT.format(name))
        dh = logging.FileHandler(debugFilePath)
        dh.setLevel(logging.DEBUG)
        dh.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        logger.addHandler(dh)
        
    return logger