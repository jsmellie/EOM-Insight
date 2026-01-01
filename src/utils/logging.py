import datetime
import logging
import os

import utils.constants as constants

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

'''Sets up the root logger for the application.'''
@run_once
def setup_root_logger(logLevel=constants.DEFAULT_LOG_LEVEL):
    
    logFolderName = 'logs'
    
    curDir = os.path.dirname(os.path.realpath(__file__))
    logFolder = os.path.join(curDir, '..', '..', logFolderName)
    if not os.path.exists(logFolder):
        os.makedirs(logFolder)
        
    # Log file name is based on date to make tracking easier
    formattedTime = datetime.datetime.now().strftime('%Y-%m-%d')
    fileNameFormat = f'general_{formattedTime}.log'
    localFilePath = os.path.join(logFolder, fileNameFormat)
        
    root = logging.getLogger()
    root.setLevel(logLevel)
    
    # Add a blank line in the log file to separate runs
    osFilePath = os.path.join(logFolder, fileNameFormat)
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
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    root.addHandler(ch)
    root.addHandler(fh)
    pass