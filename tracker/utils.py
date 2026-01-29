from datetime import datetime
from tracker.types import ExpenseSummary, ExpenseFilters, ValidatedFilters
from tracker.models import Expense
from tracker.logger import logger


def generateExpenseId(dateStr: str, no: int) -> str:
    date = datetime.fromisoformat(dateStr)
    return f"EXP-{date.year}{date.month:02d}{date.day:02d}-{no:04d}"


def validateDate(dateStr: str) -> bool:
    try:
        datetime.strptime(dateStr, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validateMonth(dateStr: str) -> bool:
    try:
        datetime.strptime(dateStr, "%Y-%m")
        return True
    except ValueError:
        return False


def format_table(expenses: list[Expense]) -> list[str]:
    lines = []
    header = f"{'ID':<17} {'Date':<12} {'Category':<15} {'Amount':>10}  {'Note'}"
    lines.append(header)

    for exp in expenses:
        lines.append(
            f"{exp['id']:<17} "
            f"{exp['date']:<12} "
            f"{exp['category']:<15} "
            f"{exp['amount']:>10.2f}  "
            f"{exp['note']}"
        )
    return lines


def format_csv(expenses: list[Expense]) -> list[str]:
    lines = []
    header = "ID,Date,Category,Amount,Note"
    lines.append(header)

    for exp in expenses:
        lines.append(
            f"{exp['id']},"
            f"{exp['date']},"
            f"{exp['category']},"
            f"{exp['amount']:.2f},"
            f"{exp['note']}"
        )
    return lines


def print_summary(summary: ExpenseSummary) -> list[str]:
    lines = []
    title = f"Summary ({summary['month']})"
    lines.append(title)
    lines.append(f"Total Expenses: {summary["total_expenses"]}")
    lines.append(f"Grand Amount: {summary['grand_total']:.2f} {summary['currency']}")
    lines.append("")
    lines.append("By Category:")
    for category, total in summary["category_totals"].items():
        lines.append(f"{category:<15} " f"{total:>15.2f} {summary['currency']}")
    lines.append("")
    lines.append(
        f"Average per day in a month: {summary['average_per_day']:.2f} {summary['currency']}"
    )
    lines.append("")
    lines.append("Highest Expense:")
    lines.append(
        f"{summary['highest_expense']['date']}  |   {summary['highest_expense']['category']}    |   {summary['highest_expense']['amount']} {summary['currency']}"
    )
    lines.append("")
    lines.append("Category Percentages:")
    for category, percentage in summary["category_percentages"].items():
        lines.append(f"{category:<15} " f"{percentage:>14.2f}%")
    return lines


def validateFilters(filters: ExpenseFilters):
    month = filters["month"] or datetime.today().date().isoformat()[:7]
    if month and not validateMonth(month):
        raise ValueError("Invalid month format. Please use YYYY-MM.")

    sort = filters["sort"] or "date"
    if sort and sort not in ["date", "amount", "category"]:
        raise ValueError("Invalid sort key. Must be one of: date, amount, category.")
    from_date = filters["from"] or None
    to_date = filters["to"] or None
    category = filters["category"] != None and filters["category"].lower() or None
    min_amount = filters["min"] or None
    max_amount = filters["max"] or None
    limit = filters["limit"] or None
    sort_direction = filters["desc"] and -1 or 1

    if from_date and not validateDate(from_date):
        raise ValueError("Invalid 'from' date format. Please use YYYY-MM-DD.")
    if to_date and not validateDate(to_date):
        raise ValueError("Invalid 'to' date format. Please use YYYY-MM-DD.")
    if from_date and to_date and to_date < from_date:
        raise ValueError("'to' date cannot be earlier than 'from' date.")
    if min_amount is not None and min_amount < 0:
        raise ValueError("Minimum amount cannot be negative.")
    if max_amount is not None and max_amount < 0:
        raise ValueError("Maximum amount cannot be negative.")
    if max_amount is not None and min_amount is not None and max_amount < min_amount:
        raise ValueError("Maximum amount cannot be less than minimum amount.")
    if limit and limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    return ValidatedFilters(
        month=month,
        sort=sort,
        from_date=from_date,
        to_date=to_date,
        category=category.lower() if category else None,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        sort_direction=sort_direction,
    )


def log_command(command_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            from tracker.logger import logger

            # Filter out None arguments for clean logging
            if args:
                arg_dict = {k: v for k, v in vars(args[0]).items() if v is not None}
            else:
                arg_dict = {}
            if kwargs:
                arg_dict.update({k: v for k, v in kwargs.items() if v is not None})

            logger.info("Command: '%s' | Args: %s", command_name, arg_dict)

            try:
                result = func(*args, **kwargs)
                logger.info("Command '%s' completed successfully", command_name)
                return result
            except Exception as e:
                # Log only the exception message, no full stack trace
                logger.error(
                    "Error in command '%s' | Args: %s | Error: %s",
                    command_name,
                    arg_dict,
                    str(e),
                )
                # Optionally print to CLI as well
                print(f"Error: {e}")
                # raise  # re-raise if you want the program to exit with error
                import sys

                sys.exit(1)

        return wrapper

    return decorator
