import os
import json

DATA_FILE = "./data/expenses.json"


def save(expense_dict):
    """
    Save an expense to the JSON storage file.

    Args:
        expense_dict: Dictionary containing expense data to save

    Returns:
        dict: The saved expense dictionary
    """
    os.makedirs("./data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"version": "1.0", "expenses": []}, f, indent=4)

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Expense data file is corrupted.")

    data["expenses"].append(expense_dict)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return expense_dict


def load():
    """
    Load all expenses from the JSON storage file.

    Args:
        None

    Returns:
        dict: The full data structure containing expenses and metadata
    """
    os.makedirs("./data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"version": "1.0", "expenses": []}, f, indent=4)

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise e
    return data
    # end try
