import datetime

class Transaction:
    date: datetime.date | None
    sum: str | None
    value: float | None
    category: str | None
    
    def __init__(self,
                 date,
                 sum,
                 value,
                 category=None):
        self.date = date
        self.sum = sum
        self.value = value
        self.category = category
        
    def __str__(self):
        return f"Transaction (D:{self.date}, S:{self.sum}, V:{self.value} - C:{self.category})"