import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(prog="tracker")

    # add subcommand
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_add = subparsers.add_parser('add', help="to add a expense")
    parser_add.add_argument('--date', type=str, help='Set a start date in YYYY-MM-DD format')
    parser_add.add_argument('--category', type=str, help="include category name", required=True)
    parser_add.add_argument('--amount', type=float, help="expense amount", required=True)
    parser_add.add_argument('--note', type=str, help="add a note")

    # list subcommand
    parser_list = subparsers.add_parser('list', help="show expenses with filters")
    parser_list.add_argument('--month', type=str, help='filter by that month - format: YYYY-MM')
    parser_list.add_argument('--from', type=str, help='from the day of the month - format: YYYY-MM-DD')
    parser_list.add_argument('--to', type=str, help='to the day of the month - format: YYYY-MM-DD')
    parser_list.add_argument('--category', type=str, help="filter by category name")
    parser_list.add_argument('--min', type=float, help="filter by min amount")
    parser_list.add_argument('--max', type=float, help="filter by max amount")
    parser_list.add_argument('--sort', type=str, help="one of: date, amount, category (default: date)")
    parser_list.add_argument('--limit', type=int, help="integer limit")
    parser_list.add_argument('--format', type=str, help="view in table or csv format")

    #summary subcommand
    parser_summary = subparsers.add_parser('summary', help="show summary with filters")
    parser_summary.add_argument('--month', type=str, help='filter by that month - format: YYYY-MM')
    parser_summary.add_argument('--from', type=str, help='from the day of the month - format: YYYY-MM-DD')
    parser_summary.add_argument('--to', type=str, help='to the day of the month - format: YYYY-MM-DD')
    parser_summary.add_argument('--category', type=str, help="filter by category name")
    parser_summary.add_argument('--min', type=float, help="filter by min amount")
    parser_summary.add_argument('--max', type=float, help="filter by max amount")
    parser_summary.add_argument('--sort', type=str, help="one of: date, amount, category (default: date)")
    parser_summary.add_argument('--limit', type=int, help="integer limit")
    parser_summary.add_argument('--format', type=str, help="view in table or csv format")


    args = parser.parse_args()

    try:
        if args.command == 'add':
            from .service import ExpenseService
            result = ExpenseService.add_expense(
                date=args.date or datetime.today().date().isoformat(),
                category=args.category,
                amount=args.amount,
                note=args.note or "N/A"
            )
            if result:
                print(result)
            else:
                print("Failed to add expense.")

        elif args.command == 'list':
            from .service import ExpenseService
            filters = {
                "month": args.month,
                "from": args.__dict__.get('from'),
                "to": args.to,
                "category": args.category,
                "min": args.min,
                "max": args.max,
                "sort": args.sort,
                "limit": args.limit,
                "format": args.format
            }
            expenses = ExpenseService.list_expenses(filters)
            
            if args.format and args.format == "csv":
                from .utils import format_csv
                lines = format_csv(expenses)
            else:
                from .utils import format_table
                lines = format_table(expenses)
            for line in lines:
                print(line)

    except ValueError as e:
        parser.error(str(e))
