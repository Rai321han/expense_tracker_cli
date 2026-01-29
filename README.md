# Expense Tracker CLI

A command-line application to manage and track your personal expenses efficiently. Built with Python, this tool allows you to add, edit, delete, and analyze your expenses with powerful filtering and reporting features.

## Features

- **Add Expenses**: Quickly add new expenses with date, category, amount, and notes
- **Edit Expenses**: Update existing expenses by ID
- **Delete Expenses**: Remove expenses from your records
- **List Expenses**: View expenses with advanced filtering and sorting options
- **Generate Summaries**: Get detailed analytics including:
  - Total expenses by category
  - Average spending per day
  - Category-wise percentage breakdown
  - Highest expense tracking
- **Multiple Output Formats**: View data in table or CSV format
- **Date Range Filtering**: Filter by month, specific date ranges, or custom periods
- **Smart Sorting**: Sort by date, amount, or category in ascending or descending order
- **Comprehensive Logging**: All commands are logged for audit trail

## Installation

### Prerequisites

- Python 3.12 or higher

### Setup

1. Clone the project directory:
```bash
git clone https://github.com/Rai321han/expense_tracker_cli.git
```

2. Move to project directory
```bash
cd expense_tracker_cli
```

3. Create and activate a virtual environment:
```bash
python -m venv .venv
```

4. Activate virtual environment

#### windows
```bash
source .venv\Scripts\activate
```

#### linux

```bash
source .venv/bin/activate
```

## Usage

### Running the Application

```bash
python -m tracker <command> [options]
```

### Available Commands

#### 1. Add an Expense

```bash
python -m tracker add --category "Food" --amount 50.00 --date "2026-01-29" --note "Lunch"
```

**Options:**
| Arguments | Description|
| - | - |
| `--category` | (required): Expense category name |
| `--amount` | (required): Expense amount |
| `--date` | (optional): Date in YYYY-MM-DD format (defaults to today) |
| `--note` | (optional): Additional note for the expense |

#### 2. List Expenses

```bash
python -m tracker list --from "2026-01-01" --to "2026-01-31" --category "Food" --min 10 --max 100 --sort "date" --limit 10 --format "table" --desc
```

**Options:**
| options | description|
| - | - |
| `--month`| Filter by month in YYYY-MM format |
| `--from`| Start date in YYYY-MM-DD format |
| `--to`| End date in YYYY-MM-DD format |
| `--category`| Filter by category name |
| `--min`| Filter by minimum amount |
| `--max`| Filter by maximum amount |
| `--sort`| Sort key: `date`, `amount`, or `category` (default: `date`) |
| `--limit`| Maximum number of expenses to display |
| `--format`| Output format: `table` or `csv` (default: `table`) |
| `--desc`| Display in descending order (default: ascending) |

> [!NOTE]
> `--month` and `--from`, `--to` will not work together. If none present, by default month will be current month

#### 3. Edit an Expense

```bash
python -m tracker edit --id "EXP-20260129-0001" --date "2026-01-29" --category "Food" --amount 60.00 --note "Updated note"
```

**Options:**
| options | description|
| - | - |
| `--id`| (required): Expense ID to update|
| `--date`| (optional): New date|
| `--category`| (optional): New category|
| `--amount`| (optional): New amount|
| `--note`| (optional): New note|

#### 4. Delete an Expense

```bash
python -m tracker delete --id "EXP-20260129-0001"
```

**Options:**
| options | description|
| - | - |
| `--id` | (required): Expense ID to delete |

#### 5. Generate Summary

```bash
python -m tracker summary --from "2026-01-01" --to "2026-01-31" --category "Food"
```

**Options:**
- Same filtering options (`--from`, `--to`, `--month`, `--category`) as `list` command
- Displays aggregated data including totals, averages, and category breakdowns

> [!NOTE]
> `--month` and `--from`, `--to` will not work together. If none present, by default month will be current month


## Examples

### Add a grocery expense
```bash
python -m tracker add --category "Groceries" --amount 75.50 --date "2026-01-29" --note "Weekly shopping"
```

### View all January 2026 expenses in table format
```bash
python -m tracker list --month "2026-01"
```

### List expenses in CSV format sorted by amount (descending)
```bash
python -m tracker list --format "csv" --sort "amount" --desc
```

### Filter expenses between $20-100 in Food category
```bash
python -m tracker list --category "Food" --min 20 --max 100
```

### Get a summary for January with category breakdown
```bash
python -m tracker summary --month "2026-01"
```

### Edit an expense
```bash
python -m tracker edit --id "EXP-20260129-0001" --amount 85.00
```

### Delete an expense
```bash
python -m tracker delete --id "EXP-20260129-0001"
```

## Project Structure

```
expense_tracker_cli/
├── README.md              # Project documentation
├── data/                  # Generate automatically
│   └── expenses.json      # JSON file storing all expenses
├── logs/                  # Generate automatically
│   └── tracker.log        # Application logs
└── tracker/
    ├── __init__.py        # Package initialization
    ├── __main__.py        # Entry point
    ├── cli.py             # Command-line interface and argument parsing
    ├── models.py          # Data models (Expense class)
    ├── service.py         # Business logic for expense operations
    ├── storage.py         # File I/O operations for JSON storage
    ├── logger.py          # Logging configuration
    ├── types.py           # Type definitions and interfaces
    └── utils.py           # Utility functions (validation, formatting)
```

## Data Storage

Expenses are stored in `data/expenses.json` with the following structure:

```json
{
  "version": "1.0",
  "expenses": [
    {
      "id": "EXP-20260129-0001",
      "date": "2026-01-29",
      "category": "Food",
      "amount": 50.00,
      "note": "Lunch",
      "currency": "BDT",
      "created_at": "2026-01-29T12:30:45.123456"
    }
  ]
}
```

## Logging

All commands are logged to `logs/tracker.log` with timestamps and execution details. This helps track:
- Command execution time
- Command arguments used
- Success or failure status
- Any errors encountered

## Error Handling

The application includes comprehensive error handling for:
- Invalid date formats
- Invalid amount values (negative numbers)
- Non-existent expense IDs
- Invalid filter parameters

## Development

### Code Structure

- **cli.py**: Handles argument parsing and routing to appropriate handlers
- **service.py**: Contains business logic for CRUD operations
- **storage.py**: Manages file I/O operations
- **utils.py**: Utility functions for validation, formatting, and logging
- **models.py**: Data models and classes
- **types.py**: Type annotations and interfaces
- **logger.py**: Logging configuration


**Last Updated**: January 29, 2026
