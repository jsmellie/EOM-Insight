from transaction import Transaction
import datetime

import logging
logger = logging.getLogger(__name__)

def validate_csv(file):
    ''' TD Credit format is as follows
    # [Month #] [Day #] [Year #] [Desc] [Debit $] [Credit $] [Balance $] '''
    
    logger.info("Validating CSV data")
    sp = file.tell()
    try:
        file.seek(0)
        lineCount = 0
        for line in file:
            if line is None or len(line) == 0:
                raise ValueError(f"Invalid length for row {lineCount}")
            commaCount = line.count(',')
            if commaCount != 6:
                raise ValueError(f"Invalid number of columns for row {lineCount}. Expected 6, got {commaCount}")
            splitLine = line.strip().split(',')
            
            month = int(splitLine[0])
            if month < 1 or month > 12:
                raise ValueError(f"Invalid month value '{month}' for row {lineCount}")
            day = int(splitLine[1])
            if day < 1 or day > 31:
                raise ValueError(f"Invalid day value '{day}' for row {lineCount}")
            year = int(splitLine[2])
            if year < 1900 or year > datetime.datetime.now().year:
                raise ValueError(f"Invalid year value '{year}' for row {lineCount}")
            desc = splitLine[3]
            if desc is None or len(desc) == 0:
                raise ValueError(f"Invalid description value for row {lineCount}")
            debit = splitLine[4]
            credit = splitLine[5]
            if (debit is None or len(debit) == 0) and (credit is None or len(credit) == 0):
                raise ValueError(f"Invalid debit and credit values for row {lineCount}")
            lineCount += 1
    except Exception as e:
        logger.exception(str(e))
        return False
    
    file.seek(sp)
    return True

def preprocess_csv(file):
    logger.info("No pre-processing needed defined")
    # Add any necessary preprocessing logic here
    return file

def import_csv(rows):
    logger.info("Starting CSV import")
    # TD Credit format is as follows
    # [Month #] [Day #] [Year #] [Desc] [Debit $] [Credit $] [Balance $]
    formatedData = []
    for row in rows:
        date = datetime.date(
            int(row[2]),
            int(row[0]),
            int(row[1])
        )
        credit = float(row[5]) if row[5] else 0.0
        debit = float(row[4]) if row[4] else 0.0
        formatedData.append(Transaction(date, row[3], credit - debit))
        
    logger.debug("Formatted Transactions:")
    i = 0
    for t in formatedData:
        logger.debug(f"R{i}: {t}")
        i += 1
        
    logger.info("CSV import successful")

    return formatedData