import os
import json

def save(expense_dict):
    # check if expenses.json exists
    if not os.path.exists('./data/expenses.json'):
        with open('./data/expenses.json', 'a') as f:
            # add {
            # 'version': '1.0',
            # 'expenses': []
            # }
            f.write('{"version": "1.0", "expenses": []}')
    with open('./data/expenses.json', 'r') as f:
        data = json.load(f)
    data['expenses'].append(expense_dict)
    with open('./data/expenses.json', 'w') as f:
        json.dump(data, f, indent=4)
    return True