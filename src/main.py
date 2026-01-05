

from pathlib import Path
import os
import csv
import logging
import datetime
import argparse
import pdfplumber
import categorizing.category_manager as category_manager

import utils.constants as constants

import parsing.csv.td_credit as td_credit
import utils.logging as logging_utils

logger = None


""" Full list of all supported institutions.  Used heavily in formatting the CSV"""
class SupportedInstitutions:
    TD_CREDIT = "TD-Credit"
    # TD_BANKING = "TD-Banking"
    # RBC_CREDIT = "RBC-Credit"
    # RBC_BANKING = "RBC-Banking"
    # EQ_BANK = "EQ-Bank"
    # CTFS_CREDIT = "CTFS-Credit"
    
def import_csv(p) -> list:
        with p.open('r', encoding='utf-8') as file:
            
            # Determine the institution type
            basename = p.stem
            parts = basename.split('_')
            instituteType = parts[0] if parts else ''
            logger.info(f"Detected institution type: {instituteType}")
            
            validate_func = None      
            preprocess_func = None
            import_func = None
            
            match instituteType:
                case SupportedInstitutions.TD_CREDIT:
                    validate_func = td_credit.validate_csv
                    preprocess_func = td_credit.preprocess_csv
                    import_func = td_credit.import_csv
                case _:
                    raise ValueError(f"The institution type '{instituteType}' is not supported.")
                
            isValid = validate_func(file)
            if not isValid:
                raise ValueError(f"The CSV file at {p} is not valid for institution type '{instituteType}'.")
            
            file = preprocess_func(file)
            reader = csv.reader(file)
            rows = list(reader)
            logger.debug(f"Imported {len(rows)} rows from {p}")
            transactions = import_func(rows)
         
            return transactions
         
def import_pdf(p) -> list:
    with p.open('rb') as file:
        logger.info(f"Importing PDF file at {p}")
        with pdfplumber.open(file) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"Total pages in PDF: {total_pages}")
            for i, page in enumerate(pdf.pages):
                text = page.extract_tables()
                logger.info(f"Tables from page {i+1}:\n{text}")
    return None

def import_file(fp) -> list:

    p = Path(fp)
    
    transactions = None
    
    try:
        if not p.exists():
            raise FileNotFoundError(f"The file at {fp} does not exist.")
        if not p.is_file():
            raise IsADirectoryError(f"The path {fp} is a directory.")
        if not os.access(fp, os.R_OK):
            raise PermissionError(f"The file at {fp} is not readable.")
        if os.path.getsize(fp) == 0:
            raise ValueError(f"The file at {fp} is empty.")
        
        fileType = p.suffix.lower()
        
        
        match fileType:
            case '.csv':
                transactions = import_csv(p)
            # case '.pdf':
                # data = import_pdf(p)
            case _:
                raise ValueError(f"The file type '{fileType}' is not supported.")
    except Exception as e:
        logger.exception(str(e))
        
    return transactions

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
    parser.add_argument('-l', '--logLevel', type=str, help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)', required=False, default=constants.DEFAULT_LOG_LEVEL)
    args = parser.parse_args()
    
    if (args.debug):
        constants.DEBUG_ENABLED = True
        
    if not is_valid_log_type(args.logLevel):
        print(f"Invalid log level provided: {args.logLevel}. Defaulting to {constants.DEFAULT_LOG_LEVEL}.")
        args.logLevel = constants.DEFAULT_LOG_LEVEL
    logging_utils.setup_root_logger(args.logLevel.upper())
    
    logger = logging_utils.create_logger(__name__) 
    
    category_manager.load_categories()
    
    file = None
    if args.file:
        logger.info(f"File provided: {args.file}")
        file = args.file
    elif constants.DEBUG_ENABLED: 
        curDir = os.path.dirname(os.path.realpath(__file__))
        testFileName = os.path.join('csv','valid','TD-Credit_Transactions_Oct2025.csv')
        file = os.path.join(curDir, '..', 'testfiles', testFileName)
        logger.info(f"Debug file: {file}")
    formatted_data = import_file(file)
    
    # TODO: Take the formatted data and categorize it
    # then split them into months
    # then update/create Google Sheets as necessary
    
    category_manager.save_categories()