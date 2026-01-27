import argparse
# from .service import add_expense, list_expenses

def main():
    parser = argparse.ArgumentParser(prog="tracker")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add")
    add.add_argument("amount", type=float)
    add.add_argument("category")

    sub.add_parser("list")

    args = parser.parse_args()

    # if args.command == "add":
    #     add_expense(args.amount, args.category)
    # elif args.command == "list":
    #     list_expenses()
    parser.print_help()
