
import datetime


def generateExpenseId(dateStr, no):
    date = datetime.datetime.fromisoformat(dateStr)
    return f"EXP-{date.year}{date.month:02d}{date.day:02d}-{no:04d}"

def validateDate(dateStr):
    try:
        datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def validateMonth(dateStr):
    try:
        datetime.datetime.strptime(dateStr, '%Y-%m')
        return True
    except ValueError:
        return False

def format_table(expenses):
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

def format_csv(expenses):
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

def print_summary(summary):
    lines = []
    title = f"Summary ({summary['month']})"
    lines.append(title)
    lines.append(f"Total Expenses: {summary['total_expenses']}")
    lines.append(f"Grand Amount: {summary['grand_total']:.2f} {summary['currency']}")
    lines.append("")
    lines.append("By Category:")
    for category, total in summary['category_totals'].items():
        lines.append(
            f"{category:<15} "
            f"{total:>15.2f} {summary['currency']}"
        )
    lines.append("")
    lines.append(f"Average per Day: {summary['average_per_day']:.2f} {summary['currency']}")
    lines.append("")
    lines.append("Highest Expense:")
    lines.append(
        f"{summary['highest_expense']['date']}  |   {summary['highest_expense']['category']}    |   {summary['highest_expense']['amount']} {summary['currency']}"
    )
    lines.append("")
    lines.append("Category Percentages:")
    for category, percentage in summary['category_percentages'].items():
        lines.append(
            f"{category:<15} "
            f"{percentage:>14.2f}%"
        )
    return lines
