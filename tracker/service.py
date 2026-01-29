import calendar
from datetime import datetime
import json
from tracker.models import Expense
from tracker.storage import save, load
from tracker.utils import generateExpenseId, validateDate, validateFilters
from tracker.types import ExpenseFilters, ExpenseSummary


class ExpenseService:
    def add_expense(date: str, category: str, amount: float, note: str) -> Expense:
        """
        Add a new expense to the storage.

        Args:
            date: Expense date in YYYY-MM-DD format
            category: Expense category name
            amount: Expense amount (must be non-negative)
            note: Additional note for the expense

        Returns:
            Expense: The saved expense object
        """
        if not validateDate(date):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        # get last expense number from storage to generate next id no
        data = load()
        expenses = data["expenses"]
        last_no = 0

        # take the last expense and extract the number
        if len(expenses) > 0:
            last_expense = expenses[-1]
            last_id = last_expense["id"]
            last_no = int(last_id.split("-")[-1])

        next_no = last_no + 1

        expense = Expense(
            id=generateExpenseId(date, next_no),
            date=date,
            category=category,
            amount=amount,
            note=note,
        )

        savedExpense = save(expense.to_dict())
        return savedExpense

    def edit_expense(
        id: str, date: str, category: str, amount: float, note: str
    ) -> Expense:
        """
        Edit an existing expense by ID.

        Args:
            id: Expense ID to update
            date: New date in YYYY-MM-DD format (optional)
            category: New category name (optional)
            amount: New amount (optional)
            note: New note (optional)

        Returns:
            Expense: The updated expense object
        """
        if date and not validateDate(date):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if amount and amount < 0:
            raise ValueError("Amount cannot be negative.")

        data = load()

        expenses = data["expenses"]
        for idx, exp in enumerate(expenses):
            if exp["id"] == id:
                expenses[idx]["date"] = date or expenses[idx]["date"]
                expenses[idx]["category"] = category or expenses[idx]["category"]
                expenses[idx]["amount"] = amount or expenses[idx]["amount"]
                expenses[idx]["note"] = note or expenses[idx]["note"]
                # save back
                with open("./data/expenses.json", "w") as f:
                    json.dump(data, f, indent=4)
                return expenses[idx]
        raise ValueError(f"Expense with ID {id} not found.")

    def delete_expense(id: str) -> Expense:
        """
        Delete an expense by ID.

        Args:
            id: Expense ID to delete

        Returns:
            Expense: The deleted expense object
        """
        data = load()
        expenses = data["expenses"]
        for idx, exp in enumerate(expenses):
            if exp["id"] == id:
                deleted_expense = expenses.pop(idx)
                with open("./data/expenses.json", "w") as f:
                    json.dump(data, f, indent=4)
                return deleted_expense
        raise ValueError(f"Expense with ID {id} not found.")

    def list_expenses(filters: ExpenseFilters) -> list[Expense]:
        """
        List expenses with optional filters and sorting.

        Args:
            filters: ExpenseFilters dict containing month, date range, category, amount range, sorting, and limit

        Returns:
            list[Expense]: List of filtered and sorted expense objects
        """
        validated = validateFilters(filters)

        month = validated.month
        from_date = validated.from_date
        to_date = validated.to_date
        category = validated.category
        min_amount = validated.min_amount
        max_amount = validated.max_amount
        sort_key = validated.sort
        limit = validated.limit
        sort_direction = validated.sort_direction

        data = load()
        expenses = data["expenses"]

        if len(expenses) == 0:
            return []

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
        filtered_expenses.sort(
            key=lambda x: x[sort_key], reverse=(sort_direction == -1)
        )
        # Apply limit
        if limit:
            filtered_expenses = filtered_expenses[:limit]
        return filtered_expenses

    def summarize_expenses(filters: ExpenseFilters) -> ExpenseSummary:
        """
        Generate a summary of expenses with analytics.

        Args:
            filters: ExpenseFilters dict to filter expenses before summarizing

        Returns:
            ExpenseSummary: Dict containing grand_total, category totals, averages, percentages, and highest expense
        """
        expenses = ExpenseService.list_expenses(filters)
        if len(expenses) == 0:
            return {"grand_total": 0, "total_expenses": 0}
        total_amount = sum(exp["amount"] for exp in expenses)
        count = len(expenses)

        category_totals = {}
        for exp in expenses:
            cat = exp["category"]
            category_totals[cat] = category_totals.get(cat, 0) + exp["amount"]

        # highest expense
        highest_expense = max(expenses, key=lambda x: x["amount"])

        # average per day
        month = filters["month"] or datetime.today().date().isoformat()[:7]
        year, month = map(int, month.split("-"))
        days_in_month = calendar.monthrange(year, month)[1]
        average_per_day = total_amount / days_in_month if days_in_month > 0 else 0

        # catergory wise percentage
        category_percentages = {}
        for cat, total in category_totals.items():
            category_percentages[cat] = (
                (total / total_amount) * 100 if total_amount > 0 else 0
            )

        summary = {
            "month": filters["month"] or datetime.today().date().isoformat()[:7],
            "grand_total": total_amount,
            "total_expenses": count,
            "category_totals": category_totals,
            "average_per_day": average_per_day,
            "category_percentages": category_percentages,
            "highest_expense": highest_expense,
            "currency": expenses[0]["currency"],
        }
        return summary
