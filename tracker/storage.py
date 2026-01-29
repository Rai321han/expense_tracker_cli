import os
import json

DATA_FILE = "./data/expenses.json"


def save(expense_dict):
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
    os.makedirs("./data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        raise FileExistsError("invalid storage")

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise e
    return data
    # end try
