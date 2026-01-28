from datetime import datetime
from tracker.models import Expense
from tracker.storage import save, load
from tracker.utils import generateExpenseId, validateDate, validateMonth

class ExpenseService:
    def add_expense(date: str, category, amount, note) -> Expense:
        if not validateDate(date):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        expense = Expense(
            id=generateExpenseId(date, 1),
            date=date,
            category=category,
            amount=amount,
            note=note
        )
        savedExpense = save(expense.to_dict())
        return f"Added: {savedExpense['id']} | {savedExpense['date']} | {savedExpense['category']} | {savedExpense['amount']} {savedExpense['currency']} | {savedExpense['note']}"


    def list_expenses(filters):
        month = filters["month"] or datetime.today().date().isoformat()[:7]
        if month and not validateMonth(month):
            raise ValueError("Invalid month format. Please use YYYY-MM.")

        sort_key = filters["sort"] or "date"
        if(sort_key and sort_key not in ["date", "amount", "category"]):
            raise ValueError("Invalid sort key. Must be one of: date, amount, category.")
        from_date = filters["from"] or None
        to_date = filters["to"] or None
        category = filters["category"] != None and filters["category"].lower() or None
        min_amount = filters["min"] or None
        max_amount = filters["max"] or None
        limit = filters["limit"] or None
        sort_direction = 1  # ascending

        if from_date and not validateDate(from_date):
            raise ValueError("Invalid 'from' date format. Please use YYYY-MM-DD.")
        if to_date and not validateDate(to_date):
            raise ValueError("Invalid 'to' date format. Please use YYYY-MM-DD.")
        if from_date and to_date and to_date < from_date:
            raise ValueError("'to' date cannot be earlier than 'from' date.")
        if min_amount and min_amount < 0:
            raise ValueError("Minimum amount cannot be negative.")
        if max_amount and max_amount < 0:
            raise ValueError("Maximum amount cannot be negative.")
        if max_amount and min_amount and max_amount < min_amount:
            raise ValueError("Maximum amount cannot be less than minimum amount.")
        if limit and limit <= 0:
            raise ValueError("Limit must be a positive integer.")
        
        data = load()
        expenses = data["expenses"]
        # Apply filters
        filtered_expenses = []
        for exp in expenses:
            if month and not exp["date"].startswith(month):
                continue
            if from_date and exp["date"] < from_date:
                continue
            if to_date and exp["date"] > to_date:
                continue
            if category and exp["category"].lower() != category:
                continue
            if min_amount and exp["amount"] < min_amount:
                continue
            if max_amount and exp["amount"] > max_amount:
                continue
            filtered_expenses.append(exp)
        
        # Sort expenses
        filtered_expenses.sort(key=lambda x: x[sort_key], reverse=(sort_direction == -1))
        # Apply limit
        if limit:
            filtered_expenses = filtered_expenses[:limit]
        return filtered_expenses
    
    # def retrieve_last_expense_id():
    #     pass