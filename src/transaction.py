from datetime import date

class Transaction:
    date: date | None
    desc: str | None
    value: float | None
    def __new__(
            cls,
            date,
            desc,
            value
    ):
        instance = super(Transaction, cls).__new__(cls)
        instance.date = date
        instance.desc = desc
        instance.value = value
        return instance
    
    def __init__(
        self,
        date,
        desc,
        value):
        self.date = date
        self.desc = desc
        self.value = value

    def __str__(self):
        return f"Transaction(Date: {self.date}, Desc: {self.desc}, Value: {self.value})"