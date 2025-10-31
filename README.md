# Personal Budget Tracker

A comprehensive Python-based budget tracker web application built with Flask for managing income and expenses with category-wise analysis and visual reports. Designed as a Major Project for Master of Computer Applications (MCA).

## Features

- ✅ **Income/Expense Tracking** - Add and manage transactions with a professional web UI
- ✅ **Dashboard** - Quick overview with total income, expenses, and balance
- ✅ **Category-wise Spending Analysis** - View spending breakdown by category with percentages
- ✅ **Monthly Reports** - Get detailed summary of income, expenses, and balance
- ✅ **Visual Charts** - Generate pie charts and bar charts for spending analysis
- ✅ **Data Persistence** - All data saved in JSON format
- ✅ **Responsive Design** - Works on desktop and mobile devices
- ✅ **Professional Structure** - Follows Flask best practices with modular architecture

## Project Structure

```
personal-budget-tracker/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Data models and database operations
│   ├── routes.py             # API routes and blueprints
│   ├── utils.py              # Utility functions for analysis and charts
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Main stylesheet
│   │   └── js/
│   │       └── main.js       # Frontend JavaScript
│   └── templates/
│       ├── base.html         # Base template
│       └── index.html        # Main page template
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── budget_data.json          # Transaction data (auto-generated)
└── README.md                 # This file
```

## Installation

1. **Install Python** (3.7 or higher)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Flask application:
```bash
python run.py
```

Then open your browser and go to: **http://localhost:5000**

### Web Interface Features

1. **Add Transaction** - Record income or expense with category and description
2. **Monthly Report** - View total income, expenses, and balance for any month
3. **All Transactions** - See all transactions in a sortable table
4. **Category Analysis** - View spending breakdown by category with percentages
5. **Charts** - Generate pie charts and bar charts for visual analysis
6. **Delete Transactions** - Remove transactions as needed

## Data Format

All transactions are stored in `budget_data.json` with the following structure:

```json
{
  "transactions": [
    {
      "type": "income",
      "amount": 5000,
      "category": "Salary",
      "description": "Monthly salary",
      "date": "2025-01-15"
    },
    {
      "type": "expense",
      "amount": 50,
      "category": "Food",
      "description": "Groceries",
      "date": "2025-01-16"
    }
  ]
}
```

## Example Workflow

1. Add your monthly income
2. Add your expenses as they occur
3. At month-end, generate a monthly report
4. View category-wise analysis to understand spending patterns
5. Generate charts for visual insights

## Output Files

- `budget_data.json` - Your transaction data
- `category_chart_YYYY_MM.png` - Pie chart of spending by category
- `income_vs_expense_YYYY_MM.png` - Bar chart comparing income vs expenses

## Requirements

- pandas - Data manipulation
- matplotlib - Chart generation
- openpyxl - Excel support (optional)
