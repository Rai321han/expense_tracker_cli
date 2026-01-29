from datetime import datetime


class Expense:
    def __init__(
        self,
        id: str,
        date: str = None,
        category: str = "",
        currency: str = "BDT",
        amount: float = 0.0,
        note: str = "",
    ):
        self.id = id
        self.date = date or datetime.today().date().isoformat()
        self.category = category
        self.amount = amount
        self.note = note
        self.currency = currency
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "note": self.note,
            "currency": self.currency,
            "created_at": self.created_at,
        }
