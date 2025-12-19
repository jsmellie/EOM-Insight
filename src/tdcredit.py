from transaction import Transaction
import datetime

import logging
logger = logging.getLogger(__name__)

def validateCSV(file):
    # TD Credit format is as follows
    # [Month #] [Day #] [Year #] [Desc] [Debit $] [Credit $] [Balance $]
    
    # Though this is probably fool hearted, I'm going to presume that the file has been validated to actually exist...
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
            lineCount += 1
                # In theory I could type check every single element but I really really don't want to...  We;ll see if I come to regret this
    except Exception as e:
        logger.exception(str(e))
        return False
    
    file.seek(sp)
    return True

def preprocessCSV(file):
    logger.info("No pre-processing needed defined")
    # Add any necessary preprocessing logic here
    return file

def importCSV(rows):
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
        
    i = 0
    for t in formatedData:
        logger.debug(f"Formatted Transaction for Row {i}: {t}")
        i += 1

    return formatedData