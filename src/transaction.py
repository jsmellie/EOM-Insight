from datetime import date

class Transaction:
    date: date | None
    sum: str | None
    value: float | None
    def __new__(
            cls,
            date,
            sum,
            value
    ):
        instance = super(Transaction, cls).__new__(cls)
        instance.date = date
        instance.sum = sum
        instance.value = value
        return instance
    
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