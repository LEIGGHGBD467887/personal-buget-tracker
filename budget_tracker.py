import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json

DATA_FILE = "budget_data.json"

def load_data():
    """Load budget data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"transactions": []}

def save_data(data):
    """Save budget data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_transaction(transaction_type, amount, category, description, date=None):
    """Add a new transaction"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    data = load_data()
    transaction = {
        "type": transaction_type,  # "income" or "expense"
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    data["transactions"].append(transaction)
    save_data(data)
    print(f"✓ {transaction_type.capitalize()} added: {category} - ${amount} on {date}")

def view_all_transactions():
    """Display all transactions"""
    data = load_data()
    if not data["transactions"]:
        print("No transactions found.")
        return
    
    df = pd.DataFrame(data["transactions"])
    print("\n" + "="*70)
    print("ALL TRANSACTIONS")
    print("="*70)
    print(df.to_string(index=False))
    print("="*70 + "\n")

def get_monthly_summary(year, month):
    """Get income and expense summary for a specific month"""
    data = load_data()
    df = pd.DataFrame(data["transactions"])
    
    if df.empty:
        print("No transactions found.")
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    target_month = pd.Period(f"{year}-{month:02d}", freq='M')
    monthly_data = df[df['year_month'] == target_month]
    
    if monthly_data.empty:
        print(f"No transactions found for {year}-{month:02d}")
        return None
    
    income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
    expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
    balance = income - expenses
    
    return {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "data": monthly_data
    }

def category_wise_analysis(year, month):
    """Analyze spending by category"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return
    
    monthly_data = summary['data']
    expenses = monthly_data[monthly_data['type'] == 'expense']
    
    if expenses.empty:
        print(f"No expenses found for {year}-{month:02d}")
        return
    
    category_spending = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    print(f"\n{'='*50}")
    print(f"CATEGORY-WISE SPENDING - {year}-{month:02d}")
    print(f"{'='*50}")
    for category, amount in category_spending.items():
        percentage = (amount / summary['expenses']) * 100
        print(f"{category:.<30} ${amount:>8.2f} ({percentage:>5.1f}%)")
    print(f"{'='*50}\n")
    
    return category_spending

def monthly_report(year, month):
    """Generate monthly report"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return
    
    print(f"\n{'='*50}")
    print(f"MONTHLY REPORT - {year}-{month:02d}")
    print(f"{'='*50}")
    print(f"Total Income:    ${summary['income']:>10.2f}")
    print(f"Total Expenses:  ${summary['expenses']:>10.2f}")
    print(f"Balance:         ${summary['balance']:>10.2f}")
    print(f"{'='*50}\n")

def plot_category_chart(year, month):
    """Create pie chart for category-wise spending"""
    category_spending = category_wise_analysis(year, month)
    if category_spending is None or category_spending.empty:
        return
    
    plt.figure(figsize=(10, 6))
    plt.pie(category_spending.values, labels=category_spending.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'Category-wise Spending - {year}-{month:02d}')
    plt.tight_layout()
    plt.savefig(f'category_chart_{year}_{month:02d}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved as 'category_chart_{year}_{month:02d}.png'")
    plt.show()

def plot_income_vs_expense(year, month):
    """Create bar chart comparing income vs expenses"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return
    
    categories = ['Income', 'Expenses']
    amounts = [summary['income'], summary['expenses']]
    colors = ['#2ecc71', '#e74c3c']
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts, color=colors, width=0.5)
    plt.ylabel('Amount ($)')
    plt.title(f'Income vs Expenses - {year}-{month:02d}')
    plt.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(amounts):
        plt.text(i, v + 50, f'${v:.2f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'income_vs_expense_{year}_{month:02d}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved as 'income_vs_expense_{year}_{month:02d}.png'")
    plt.show()

def main_menu():
    """Display main menu"""
    while True:
        print("\n" + "="*50)
        print("PERSONAL BUDGET TRACKER")
        print("="*50)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Monthly Report")
        print("5. Category-wise Analysis")
        print("6. View Charts")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            amount = float(input("Enter income amount: $"))
            category = input("Enter category (e.g., Salary, Bonus): ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            add_transaction("income", amount, category, description, date if date else None)
        
        elif choice == '2':
            amount = float(input("Enter expense amount: $"))
            category = input("Enter category (e.g., Food, Transport, Utilities): ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            add_transaction("expense", amount, category, description, date if date else None)
        
        elif choice == '3':
            view_all_transactions()
        
        elif choice == '4':
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            monthly_report(year, month)
        
        elif choice == '5':
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            category_wise_analysis(year, month)
        
        elif choice == '6':
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            print("\n1. Category-wise Pie Chart")
            print("2. Income vs Expense Bar Chart")
            chart_choice = input("Choose chart (1-2): ").strip()
            if chart_choice == '1':
                plot_category_chart(year, month)
            elif chart_choice == '2':
                plot_income_vs_expense(year, month)
            else:
                print("Invalid choice!")
        
        elif choice == '7':
            print("Thank you for using Budget Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
