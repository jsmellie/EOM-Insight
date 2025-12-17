

def importCSV(filePath):
    from pathlib import Path
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
        
        # parse CSV into a list of rows
        reader = csv.DictReader(file)
        rows = list(reader)
        print (f"Imported {len(rows)} rows from {filePath}")
        
        basename = p.stem
        print (f"Basename: {basename}")
        
        parts = basename.split('_')
        instituteType = parts[0] if parts else ''
        print (f"Institute Type: {instituteType}")
        
        match instituteType:
            case 'TD-Credit':
                #importTDCreditCSV(data)
                pass
            case 'TD-Banking':
                #importTDBankingCSV(data)
                pass
            case 'RBC-Credit':
                #importRBCCreditCSV(data)
                pass
            case 'EQ-Bank':
                #importEQBankCSV(data)
                pass
            case 'CTFS-Credit':
                #importCTFSCreditCSV(data)
                pass
            
            
            
if __name__ == '__main__':
    testFilePath = 'C:/Users/Jeremy/Documents/Programing/BudgetAmalgamator/testfiles/TD-Credit_Transactions_Oct2025.csv'
    importCSV(testFilePath)