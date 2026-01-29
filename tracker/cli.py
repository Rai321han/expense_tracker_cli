import argparse
from datetime import datetime
from tracker.utils import print_summary, log_command, format_summary_csv
from tracker.logger import logger


def main():
    """
    Parse command line arguments and route to appropriate command handler.

    Args:
        None (uses sys.argv from command line)

    Returns:
        None
    """
    parser = argparse.ArgumentParser(prog="tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add subcommand
    parser_add = subparsers.add_parser("add", help="to add a expense")
    parser_add.add_argument(
        "--date", type=str, help="Set a start date in YYYY-MM-DD format"
    )
    parser_add.add_argument(
        "--category", type=str, help="include category name", required=True
    )
    parser_add.add_argument(
        "--amount", type=float, help="expense amount", required=True
    )
    parser_add.add_argument("--note", type=str, help="add a note")

    # edit subcommand
    parser_edit = subparsers.add_parser("edit", help="to edit an expense")
    parser_edit.add_argument("--id", type=str, help="expense id", required=True)
    parser_edit.add_argument(
        "--date", type=str, help="Set a start date in YYYY-MM-DD format"
    )
    parser_edit.add_argument("--category", type=str, help="include category name")
    parser_edit.add_argument("--amount", type=float, help="expense amount")
    parser_edit.add_argument("--note", type=str, help="add a note")

    # delete
    parser_delete = subparsers.add_parser("delete", help="to delete an expense")
    parser_delete.add_argument("--id", type=str, help="expense id", required=True)

    # list subcommand
    parser_list = subparsers.add_parser("list", help="show expenses with filters")
    parser_list.add_argument(
        "--month", type=str, help="filter by that month - format: YYYY-MM"
    )
    parser_list.add_argument(
        "--from", type=str, help="from the day of the month - format: YYYY-MM-DD"
    )
    parser_list.add_argument(
        "--to", type=str, help="to the day of the month - format: YYYY-MM-DD"
    )
    parser_list.add_argument("--category", type=str, help="filter by category name")
    parser_list.add_argument("--min", type=float, help="filter by min amount")
    parser_list.add_argument("--max", type=float, help="filter by max amount")
    parser_list.add_argument(
        "--sort", type=str, help="one of: date, amount, category (default: date)"
    )
    parser_list.add_argument("--limit", type=int, help="integer limit")
    parser_list.add_argument("--format", type=str, help="view in table or csv format")
    parser_list.add_argument(
        "--desc",
        action="store_true",
        help="view in descending order; default is ascending",
    )

    # summary subcommand
    parser_summary = subparsers.add_parser("summary", help="show summary with filters")
    parser_summary.add_argument(
        "--month", type=str, help="filter by that month - format: YYYY-MM"
    )
    parser_summary.add_argument(
        "--from", type=str, help="from the day of the month - format: YYYY-MM-DD"
    )
    parser_summary.add_argument(
        "--to", type=str, help="to the day of the month - format: YYYY-MM-DD"
    )
    parser_summary.add_argument("--category", type=str, help="filter by category name")
    parser_summary.add_argument("--min", type=float, help="filter by min amount")
    parser_summary.add_argument("--max", type=float, help="filter by max amount")
    parser_summary.add_argument(
        "--sort", type=str, help="one of: date, amount, category (default: date)"
    )
    parser_summary.add_argument("--limit", type=int, help="integer limit")
    parser_summary.add_argument(
        "--format", type=str, help="view in table or csv format"
    )
    parser_summary.add_argument(
        "--desc",
        action="store_true",
        help="view in descending order; default is ascending",
    )

    args = parser.parse_args()

    try:
        if args.command == "add":
            add_parser(args)

        elif args.command == "list":
            list_parser(args)

        elif args.command == "edit":
            edit_parser(args)

        elif args.command == "delete":
            delete_parser(args)

        elif args.command == "summary":
            summary_parser(args)

    except ValueError as e:
        parser.error(str(e))


@log_command("add")
def add_parser(args):
    """
    Add a new expense to the tracker.

    Args:
        args: Parsed command line arguments containing date, category, amount, and note

    Returns:
        None
    """
    from .service import ExpenseService

    try:
        result = ExpenseService.add_expense(
            date=args.date or datetime.today().date().isoformat(),
            category=args.category,
            amount=args.amount,
            note=args.note or "N/A",
        )
        if result:
            print(
                f"Added: {result['id']} | {result['date']} | {result['category']} | {result['amount']} {result['currency']} | {result['note']}"
            )
        else:
            print("Failed to add expense.")
    except Exception as e:
        raise e


@log_command("list")
def list_parser(args):
    """
    List expenses with optional filters and formatting.

    Args:
        args: Parsed command line arguments with filter options (month, from, to, category, min, max, sort, limit, format, desc)

    Returns:
        None (prints results to stdout)
    """
    from .service import ExpenseService

    filters = {
        "month": args.month,
        "from": args.__dict__.get("from"),
        "to": args.to,
        "category": args.category,
        "min": args.min,
        "max": args.max,
        "sort": args.sort or "date",
        "limit": args.limit,
        "format": args.format or "table",
        "desc": args.desc,
    }
    expenses = ExpenseService.list_expenses(filters)
    if len(expenses) == 0:
        print("No expenses found.")
        return

    if args.format and args.format == "csv":
        from .utils import format_csv

        lines = format_csv(expenses)
    else:
        from .utils import format_table

        lines = format_table(expenses)
    for line in lines:
        print(line)


@log_command("summary")
def summary_parser(args):
    """
    Display a summary of expenses with optional filters.

    Args:
        args: Parsed command line arguments with filter options (month, from, to, category, min, max, sort, limit, format, desc)

    Returns:
        None (prints summary to stdout)
    """
    from .service import ExpenseService

    filters = {
        "month": args.month,
        "from": args.__dict__.get("from"),
        "to": args.to,
        "category": args.category,
        "min": args.min,
        "max": args.max,
        "sort": args.sort or "date",
        "limit": args.limit,
        "format": args.format or "table",
        "desc": args.desc,
    }
    summary = ExpenseService.summarize_expenses(filters)
    if len(summary) == 0:
        print("No expenses found for summary.")
        return

    # lines = print_summary(summary)
    # for line in lines:
    #     print(line)
    # Decide output format
    if args.format and args.format.lower() == "csv":
        lines = format_summary_csv(summary)
        # save to a file
        csv_file = f"summary_{summary['month']}.csv"
        with open(csv_file, "w", newline="") as f:
            f.write("\n".join(lines))
        print(f"Summary exported to {csv_file}")
    else:
        # default: terminal table
        lines = print_summary(summary)
        for line in lines:
            print(line)


@log_command("edit")
def edit_parser(args):
    """
    Edit an existing expense by ID.

    Args:
        args: Parsed command line arguments containing expense id and optional fields to update (date, category, amount, note)

    Returns:
        None
    """
    from .service import ExpenseService

    result = ExpenseService.edit_expense(
        id=args.id,
        date=args.date or datetime.today().date().isoformat(),
        category=args.category,
        amount=args.amount,
        note=args.note or "N/A",
    )
    if result:
        print(
            f"Edited: {result['id']} | {result['date']} | {result['category']} | {result['amount']} {result['currency']} | {result['note']}"
        )
    else:
        print("Failed to edit expense.")


@log_command("delete")
def delete_parser(args):
    """
    Delete an expense by ID.

    Args:
        args: Parsed command line arguments containing expense id to delete

    Returns:
        None
    """
    from .service import ExpenseService

    result = ExpenseService.delete_expense(id=args.id)
    if result:
        print(
            f"Deleted: {result['id']} | {result['date']} | {result['category']} | {result['amount']} {result['currency']} | {result['note']}"
        )
    else:
        print("Failed to delete expense.")
