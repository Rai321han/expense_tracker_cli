from datetime import datetime

class ExpenseService:
    # static methods for managing expenses
    @staticmethod
    def add_expense(date, category, amount, note):
        from .storage import save
        expense_dict = {
            'date': date,
            'category': category,
            'amount': amount,
            'note': note,
            'currency': 'BDT',
            'created_at': datetime.now().isoformat()
        }
        return save(expense_dict)