
import logging
logger = logging.getLogger(__name__)

class SupportedInstitutions: # Holder class for all the institutions that we will support
    TD_CREDIT = "TD-Credit"
    # TD_BANKING = "TD-Banking"
    # RBC_CREDIT = "RBC-Credit"
    # RBC_BANKING = "RBC-Banking"
    # EQ_BANK = "EQ-Bank"
    # CTFS_CREDIT = "CTFS-Credit"

def importCSV(filePath):
    from pathlib import Path
    import tdcredit
    import os
    import csv
    import logging
    
    p = Path(filePath)
    
    try:
        if not p.exists(): # Ensure the path exists
            raise FileNotFoundError(f"The file at {filePath} does not exist.")
        if not p.is_file(): # Ensure that is is a file
            raise IsADirectoryError(f"The path {filePath} is a directory.")
        if not p.suffix.lower() == '.csv': # Ensure that it is a CSV
            raise ValueError(f"The file at {filePath} is not a CSV file.")
        if not os.access(filePath, os.R_OK): # Ensure that the file is readable
            raise PermissionError(f"The file at {filePath} is not readable.")
    
        with p.open('r', encoding='utf-8') as file:
            
            # Determine the institution type
            basename = p.stem
            parts = basename.split('_')
            instituteType = parts[0] if parts else ''
            logger.info(f"Detected institution type: {instituteType}")
            
            # Set func references based on institution type
            validateCSVFunc = None      
            preprocessCSVFunc = None
            importFunc = None
            
            match instituteType:
                case SupportedInstitutions.TD_CREDIT:
                    validateCSVFunc = tdcredit.validateCSV
                    preprocessCSVFunc = tdcredit.preprocessCSV
                    importFunc = tdcredit.importCSV
                case _:
                    raise ValueError(f"The institution type '{instituteType}' is not supported.")
                
            # Validate CSV
            isValid = validateCSVFunc(file)
            if not isValid:
                raise ValueError(f"The CSV file at {filePath} is not valid for institution type '{instituteType}'.")
            
            # Parse CSV into a list of rows
            file = preprocessCSVFunc(file)
            reader = csv.reader(file)
            rows = list(reader)
            logger.debug(f"Imported {len(rows)} rows from {filePath}")
            formatedData = importFunc(rows)
        
    except Exception as e:
        logger.exception(str(e))
        
        # ---
        # TODO List
        # - Categarize transactions based on description regex
        # - Compare valid tranactions against previous imports to prevent duplicates
        # - Update Google sheet with information
        # - Add support for more institutions
        # ---

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def setupRootLogger(logLevel=logging.INFO):
    import datetime
    import os
    
    logFolderName = 'logs'
    
    # Make sure that the log folder exists
    curDir = os.path.dirname(os.path.realpath(__file__))
    logFolder = os.path.join(curDir, '..', logFolderName)
    if not os.path.exists(logFolder):
        os.makedirs(logFolder)
        
    # Determine log file name
    formattedTime = datetime.datetime.now().strftime('%Y-%m-%d')
    fileNameFormat = f'general_{formattedTime}.log'
    localFilePath = os.path.join(logFolderName, fileNameFormat)
        
    # Create logger
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
            
def peekLine(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line        
            
if __name__ == '__main__':
    import os
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='EOM Insight CSV Importer')
    parser.add_argument('file', type=str, help='Path to the CSV file to import', nargs='?')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode', required=False)
    parser.add_argument('-l', '--logLevel', type=str, help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)', required=False, default='WARNING')
    args = parser.parse_args()
    
    if (args.debug): #We ignore the log level if debug is set
        args.logLevel = 'DEBUG'
    
    # Setup the root logger
    setupRootLogger(args.logLevel)
    
    logger.info(f"File value: {args.file}")
    
    if args.file:
        logger.info(f"File provided: {args.file}")
        importCSV(args.file)
    elif args.debug:
        # For testing purposes    
        curDir = os.path.dirname(os.path.realpath(__file__))
        testFileName = os.path.join('valid','TD-Credit_Transactions_Oct2025.csv')
        testFilePath = os.path.join(curDir, '..', 'testfiles', testFileName)
        logger.info(f"Testing importCSV with file: {testFilePath}")
        importCSV(testFilePath)