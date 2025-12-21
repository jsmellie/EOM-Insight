

from pathlib import Path
import os
import csv
import logging
import datetime
import argparse

import tdcredit

logger = logging.getLogger(__name__)

""" Full list of all supported institutions.  Used heavily in formatting the CSV"""
class SupportedInstitutions:
    TD_CREDIT = "TD-Credit"
    # TD_BANKING = "TD-Banking"
    # RBC_CREDIT = "RBC-Credit"
    # RBC_BANKING = "RBC-Banking"
    # EQ_BANK = "EQ-Bank"
    # CTFS_CREDIT = "CTFS-Credit"

def import_csv(filePath):

    p = Path(filePath)
    
    try:
        if not p.exists():
            raise FileNotFoundError(f"The file at {filePath} does not exist.")
        if not p.is_file():
            raise IsADirectoryError(f"The path {filePath} is a directory.")
        if not p.suffix.lower() == '.csv':
            raise ValueError(f"The file at {filePath} is not a CSV file.")
        if not os.access(filePath, os.R_OK):
            raise PermissionError(f"The file at {filePath} is not readable.")
    
        with p.open('r', encoding='utf-8') as file:
            
            # Determine the institution type
            basename = p.stem
            parts = basename.split('_')
            instituteType = parts[0] if parts else ''
            logger.info(f"Detected institution type: {instituteType}")
            
            validateCSVFunc = None      
            preprocessCSVFunc = None
            importFunc = None
            
            match instituteType:
                case SupportedInstitutions.TD_CREDIT:
                    validateCSVFunc = tdcredit.validate_csv
                    preprocessCSVFunc = tdcredit.preprocess_csv
                    importFunc = tdcredit.import_csv
                case _:
                    raise ValueError(f"The institution type '{instituteType}' is not supported.")
                
            isValid = validateCSVFunc(file)
            if not isValid:
                raise ValueError(f"The CSV file at {filePath} is not valid for institution type '{instituteType}'.")
            
            file = preprocessCSVFunc(file)
            reader = csv.reader(file)
            rows = list(reader)
            logger.debug(f"Imported {len(rows)} rows from {filePath}")
            formatedData = importFunc(rows)
        
    except Exception as e:
        logger.exception(str(e))
        
        ''' ---
        # TODO List
        # - Categorize transactions based on description regex
        # - Compare valid transactions against previous imports to prevent duplicates
        # - Update Google sheet with information
        # - Add support for more institutions
         --- '''

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def setup_root_logger(logLevel=logging.INFO):
    
    logFolderName = 'logs'
    
    curDir = os.path.dirname(os.path.realpath(__file__))
    logFolder = os.path.join(curDir, '..', logFolderName)
    if not os.path.exists(logFolder):
        os.makedirs(logFolder)
        
    # Log file name is based on date to make tracking easier
    formattedTime = datetime.datetime.now().strftime('%Y-%m-%d')
    fileNameFormat = f'general_{formattedTime}.log'
    localFilePath = os.path.join(logFolderName, fileNameFormat)
        
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

'''Determines if the provided log type is valid by utilizing internal dictionaries of the logging module'''
def is_valid_log_type(log_type):
    if isinstance(log_type, str):
        if (logging._nameToLevel.get(log_type.upper()) is None):
            return False
        return True
    elif isinstance(log_type, int):
        if (logging._levelToName.get(log_type) is None):
            return False
        return True
    else:
        return False 

'''Peeks at the next line in a file without advancing the file pointer'''
def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line        
           
'''Main entry point for EOM Insight''' 
if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='EOM Insight CSV Importer')
    parser.add_argument('file', type=str, help='Path to the CSV file to import', nargs='?')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode', required=False)
    parser.add_argument('-l', '--logLevel', type=str, help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)', required=False, default='WARNING')
    args = parser.parse_args()
    
    # While debugging, ensure that the log level is properly set to DEBUG
    if (args.debug):
        args.logLevel = 'DEBUG'
        
    if not is_valid_log_type(args.logLevel):
        print(f"Invalid log level provided: {args.logLevel}. Defaulting to WARNING.")
        args.logLevel = 'WARNING'
    setup_root_logger(args.logLevel.upper())
    
    logger.info(f"File value: {args.file}")
    
    file = None
    if args.file:
        logger.info(f"File provided: {args.file}")
        file = args.file
    elif args.debug:    
        curDir = os.path.dirname(os.path.realpath(__file__))
        testFileName = os.path.join('valid','TD-Credit_Transactions_Oct2025.csv')
        file = os.path.join(curDir, '..', 'testfiles', testFileName)
        logger.info(f"Debug file: {file}")
    import_csv(file)