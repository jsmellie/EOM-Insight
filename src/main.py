
class SupportedInstitutions:
    TD_CREDIT = "TD-Credit"
    TD_BANKING = "TD-Banking"
    RBC_CREDIT = "RBC-Credit"
    EQ_BANK = "EQ-Bank"
    CTFS_CREDIT = "CTFS-Credit"

def importCSV(filePath):
    from pathlib import Path
    import tdcredit
    import os
    import csv
    
    p = Path(filePath)
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
        
        # Set func references based on institution type        
        addHeaderRowFunc = None
        importFunc = None
        
        match instituteType:
            case SupportedInstitutions.TD_CREDIT:
                addHeaderRowFunc = tdcredit.preimportCSVManipulation
                importFunc = tdcredit.importCSV
            case _:
                raise ValueError(f"The institution type '{instituteType}' is not supported.")
            
        # 
        
        # Parse CSV into a list of rows
        reader = csv.DictReader(file)
        rows = list(reader)
        print (f"Imported {len(rows)} rows from {filePath}")
    
        
        formatedData = []
        
        
            
            
            
if __name__ == '__main__':
    testFilePath = 'C:/Users/Jeremy/Documents/Programming/EOM-Insight/testfiles/TD-Credit_Transactions_Oct2025.csv'
    importCSV(testFilePath)