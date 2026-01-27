import argparse
from datetime import datetime
# from .service import add_expense, list_expenses

def main():
    parser = argparse.ArgumentParser(prog="tracker")

    # add subcommand
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_add = subparsers.add_parser('add', help="to add a expense")
    parser_add.add_argument('--date', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='Set a start date in YYYY-MM-DD format')
    parser_add.add_argument('--category', type=str, help="include category name")
    parser_add.add_argument('--amount', type=float, help="expense amount")
    parser_add.add_argument('--note', type=str, help="add a note")

    # list subcommand
    parser_list = subparsers.add_parser('list', help="show expenses with filters")
    parser_list.add_argument('--month', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='filter by that month - format: YYYY-MM')
    parser_list.add_argument('--from', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='from the day of the month - format: YYYY-MM-DD')
    parser_list.add_argument('--to', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='to the day of the month - format: YYYY-MM-DD')
    parser_list.add_argument('--category', type=str, help="filter by category name")
    parser_list.add_argument('--min', type=float, help="filter by min amount")
    parser_list.add_argument('--max', type=float, help="filter by max amount")
    parser_list.add_argument('--sort', type=str, help="one of: date, amount, category (default: date)")
    parser_list.add_argument('--limit', type=int, help="integer limit")
    parser_list.add_argument('--format', type=str, help="view in table or csv format")

    #summary subcommand
    parser_summary = subparsers.add_parser('summary', help="show summary with filters")
    parser_summary.add_argument('--month', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='filter by that month - format: YYYY-MM')
    parser_summary.add_argument('--from', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='from the day of the month - format: YYYY-MM-DD')
    parser_summary.add_argument('--to', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='to the day of the month - format: YYYY-MM-DD')
    parser_summary.add_argument('--category', type=str, help="filter by category name")
    parser_summary.add_argument('--min', type=float, help="filter by min amount")
    parser_summary.add_argument('--max', type=float, help="filter by max amount")
    parser_summary.add_argument('--sort', type=str, help="one of: date, amount, category (default: date)")
    parser_summary.add_argument('--limit', type=int, help="integer limit")
    parser_summary.add_argument('--format', type=str, help="view in table or csv format")


    args = parser.parse_args()

    if args.command == 'add':
        from .service import ExpenseService
        result = ExpenseService.add_expense(
            date=args.date.isoformat() if args.date else datetime.now().date().isoformat(),
            category=args.category,
            amount=args.amount,
            note=args.note
        )
        if result:
            print("Expense added successfully.")
        else:
            print("Failed to add expense.")