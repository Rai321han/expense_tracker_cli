import datetime


def generateExpenseId(dateStr, no):
    date = datetime.datetime.fromisoformat(dateStr)
    return f"EXP-{date.year}{date.month:02d}{date.day:02d}-{no}"

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
    header = f"{'ID':<15} {'Date':<12} {'Category':<15} {'Amount':>10}  {'Note'}"
    lines.append(header)

    for exp in expenses:
        lines.append(
            f"{exp['id']:<15} "
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