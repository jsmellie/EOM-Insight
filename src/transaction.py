import datetime

class Transaction:
    date: datetime.date | None
    sum: str | None
    value: float | None
    
    def __init__(
        self,
        date,
        sum,
        value):
        self.date = date
        self.sum = sum
        self.value = value

    def __str__(self):
        return f"Transaction (D:{self.date}, S:{self.sum}, V:{self.value})"