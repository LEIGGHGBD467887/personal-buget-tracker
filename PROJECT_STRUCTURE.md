# Personal Budget Tracker - Project Structure

## Overview
This is a professional Flask-based web application following industry best practices and MCA project guidelines.

## Directory Structure

```
personal-budget-tracker/
│
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory - creates and configures the Flask app
│   ├── models.py                # Data models and database operations
│   │                            # - Transaction class
│   │                            # - BudgetDatabase class for CRUD operations
│   ├── routes.py                # API routes and blueprints
│   │                            # - Main blueprint (index route)
│   │                            # - API blueprint (REST endpoints)
│   ├── utils.py                 # Utility functions
│   │                            # - Monthly summary calculations
│   │                            # - Category analysis
│   │                            # - Chart generation (matplotlib)
│   │
│   ├── static/                  # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css        # Main stylesheet (professional design)
│   │   └── js/
│   │       └── main.js          # Frontend JavaScript (AJAX calls, DOM manipulation)
│   │
│   └── templates/               # HTML templates (Jinja2)
│       ├── base.html            # Base template with navbar and footer
│       └── index.html           # Main page template (extends base.html)
│
├── config.py                    # Configuration settings
│                                # - Development, Production, Testing configs
│
├── run.py                       # Application entry point
│                                # - Creates Flask app using factory pattern
│                                # - Starts development server
│
├── requirements.txt             # Python dependencies
│                                # - flask==2.3.3
│                                # - pandas==2.3.3
│                                # - matplotlib==3.10.7
│                                # - openpyxl==3.1.2
│
├── budget_data.json             # Data storage (auto-generated)
│                                # - JSON file storing all transactions
│
├── README.md                    # Project documentation
├── PROJECT_STRUCTURE.md         # This file
└── budget_tracker.py            # (Legacy) Original CLI version
```

## Key Components

### 1. Application Factory Pattern (`app/__init__.py`)
- Creates Flask app instance
- Loads configuration
- Registers blueprints
- Enables modular architecture

### 2. Models (`app/models.py`)
- **Transaction Class**: Represents a single transaction
- **BudgetDatabase Class**: Handles all database operations
  - `load_data()`: Load transactions from JSON
  - `save_data()`: Save transactions to JSON
  - `add_transaction()`: Add new transaction
  - `get_all_transactions()`: Retrieve all transactions
  - `delete_transaction()`: Delete transaction by index
  - `get_transactions_by_month()`: Filter by month

### 3. Routes (`app/routes.py`)
- **Main Blueprint**: Serves HTML pages
  - `GET /`: Home page
- **API Blueprint**: REST endpoints
  - `GET /api/transactions`: Get all transactions
  - `POST /api/add-transaction`: Add transaction
  - `DELETE /api/delete-transaction/<id>`: Delete transaction
  - `GET /api/monthly-report/<year>/<month>`: Monthly summary
  - `GET /api/category-analysis/<year>/<month>`: Category breakdown
  - `GET /api/chart/category/<year>/<month>`: Pie chart
  - `GET /api/chart/income-vs-expense/<year>/<month>`: Bar chart

### 4. Utilities (`app/utils.py`)
- `get_monthly_summary()`: Calculate income/expenses/balance
- `get_category_analysis()`: Analyze spending by category
- `generate_category_chart()`: Create pie chart (base64 image)
- `generate_income_vs_expense_chart()`: Create bar chart (base64 image)

### 5. Frontend
- **CSS** (`app/static/css/style.css`): Professional styling
  - Responsive design
  - Modern color scheme
  - Smooth animations
- **JavaScript** (`app/static/js/main.js`): Client-side logic
  - AJAX calls to API
  - DOM manipulation
  - Form validation
  - Tab switching

### 6. Templates
- **base.html**: Base template with navbar, footer, and block inheritance
- **index.html**: Main page extending base.html
  - Project information section
  - Add transaction form
  - Monthly report section
  - Dashboard with tabs

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | Flask 2.3.3 |
| Data Processing | Pandas 2.3.3 |
| Visualization | Matplotlib 3.10.7 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Data Storage | JSON |
| Server | Flask Development Server |
| Python Version | 3.7+ |

## Features

### 1. Dashboard
- Total income, expenses, and balance
- Top 10 spending categories
- Quick overview of financial status

### 2. Transaction Management
- Add income/expense transactions
- View all transactions in table format
- Delete transactions
- Filter by date

### 3. Monthly Reports
- Get monthly income and expenses
- Calculate balance
- View specific month data

### 4. Category Analysis
- Spending breakdown by category
- Percentage distribution
- Top spending categories

### 5. Visual Reports
- Pie chart: Category-wise spending
- Bar chart: Income vs Expenses
- Charts generated as base64 images

## Data Flow

```
User Input (HTML Form)
    ↓
JavaScript (AJAX)
    ↓
Flask API Routes
    ↓
Models (Database Operations)
    ↓
JSON File (budget_data.json)
    ↓
Utils (Analysis & Charts)
    ↓
JSON Response
    ↓
JavaScript (DOM Update)
    ↓
User sees updated UI
```

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Access at http://localhost:5000
```

## Configuration

Edit `config.py` to change:
- Debug mode
- Secret key
- Environment settings

## Project Guidelines Compliance

✅ **Modular Architecture**: Separate files for models, routes, utils
✅ **Configuration Management**: Centralized config.py
✅ **Template Inheritance**: base.html with block inheritance
✅ **Static Files**: Organized CSS and JS
✅ **RESTful API**: Proper HTTP methods and status codes
✅ **Error Handling**: Try-catch blocks and error responses
✅ **Documentation**: Comments and docstrings
✅ **Professional UI**: Modern design with responsive layout
✅ **Data Persistence**: JSON-based storage
✅ **Scalability**: Factory pattern allows easy extension

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- User authentication
- Budget goals and alerts
- Recurring transactions
- Export to PDF/Excel
- Mobile app
- Cloud deployment
