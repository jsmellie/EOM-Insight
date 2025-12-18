from datetime import date

class Transaction:
    date: date | None
    desc: str | None
    value: int
    def __new__(
            cls,
            date,
            desc,
            value
    )
    def __init__(self):
        pass