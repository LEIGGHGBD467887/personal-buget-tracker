"""
Utility functions for Budget Tracker
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import base64
from app.models import BudgetDatabase
from datetime import datetime

def get_monthly_summary(year, month):
    """Get income and expense summary for a specific month"""
    monthly_data = BudgetDatabase.get_transactions_by_month(year, month)
    
    if monthly_data is None or monthly_data.empty:
        return None
    
    income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
    expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
    balance = income - expenses
    
    return {
        "income": float(income),
        "expenses": float(expenses),
        "balance": float(balance),
        "data": monthly_data
    }

def get_category_analysis(year, month):
    """Analyze spending by category"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return None
    
    monthly_data = summary['data']
    expenses = monthly_data[monthly_data['type'] == 'expense']
    
    if expenses.empty:
        return []
    
    category_spending = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    total_expenses = category_spending.sum()
    
    categories = []
    for category, amount in category_spending.items():
        percentage = (amount / total_expenses) * 100
        categories.append({
            "category": category,
            "amount": float(amount),
            "percentage": float(percentage)
        })
    
    return categories

def generate_category_chart(year, month):
    """Generate category pie chart as base64 image"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return None
    
    monthly_data = summary['data']
    expenses = monthly_data[monthly_data['type'] == 'expense']
    
    if expenses.empty:
        return None
    
    category_spending = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    colors = plt.cm.Set3(range(len(category_spending)))
    plt.pie(category_spending.values, labels=category_spending.index, autopct='%1.1f%%', 
            startangle=90, colors=colors)
    plt.title(f'Category-wise Spending - {year}-{month:02d}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    img = BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plt.close()
    
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return f"data:image/png;base64,{img_base64}"

def generate_income_vs_expense_chart(year, month):
    """Generate income vs expense bar chart as base64 image"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return None
    
    income = summary['income']
    expenses = summary['expenses']
    
    categories = ['Income', 'Expenses']
    amounts = [income, expenses]
    colors = ['#2ecc71', '#e74c3c']
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, amounts, color=colors, width=0.5)
    plt.ylabel('Amount ($)', fontsize=12)
    plt.title(f'Income vs Expenses - {year}-{month:02d}', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    for bar, amount in zip(bars, amounts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${amount:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    img = BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plt.close()
    
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return f"data:image/png;base64,{img_base64}"

def check_budget_alert():
    """Check if expenses exceed income and return alert status"""
    data = BudgetDatabase.load_data()
    if not data["transactions"]:
        return {"alert": False, "message": "", "income": 0, "expenses": 0}
    
    total_income = 0
    total_expenses = 0
    
    for transaction in data["transactions"]:
        if transaction["type"] == "income":
            total_income += float(transaction["amount"])
        else:
            total_expenses += float(transaction["amount"])
    
    if total_expenses > total_income:
        return {
            "alert": True,
            "message": f"⚠️ WARNING: Your expenses (${total_expenses:.2f}) exceed your income (${total_income:.2f}) by ${total_expenses - total_income:.2f}!",
            "income": total_income,
            "expenses": total_expenses,
            "deficit": total_expenses - total_income
        }
    else:
        remaining = total_income - total_expenses
        return {
            "alert": False,
            "message": f"✓ Good! You have ${remaining:.2f} remaining after expenses.",
            "income": total_income,
            "expenses": total_expenses,
            "remaining": remaining
        }

def export_all_transactions_csv():
    """Export all transactions to CSV format"""
    transactions = BudgetDatabase.get_all_transactions()
    
    if not transactions:
        return None
    
    df = pd.DataFrame(transactions)
    df = df.sort_values('date', ascending=False)
    
    # Create CSV string
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    
    return csv_content

def export_monthly_report_csv(year, month):
    """Export monthly report to CSV format"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return None
    
    monthly_data = summary['data']
    
    # Create summary section
    csv_lines = [
        "MONTHLY BUDGET REPORT",
        f"Month: {year}-{month:02d}",
        "",
        "SUMMARY",
        f"Total Income,${summary['income']:.2f}",
        f"Total Expenses,${summary['expenses']:.2f}",
        f"Balance,${summary['balance']:.2f}",
        "",
        "TRANSACTIONS",
    ]
    
    # Add transactions
    df = monthly_data.sort_values('date', ascending=False)
    csv_lines.append(df.to_csv(index=False))
    
    csv_content = "\n".join(csv_lines)
    return csv_content

def export_category_analysis_csv(year, month):
    """Export category analysis to CSV format"""
    categories = get_category_analysis(year, month)
    if categories is None or not categories:
        return None
    
    # Create CSV content
    csv_lines = [
        "CATEGORY-WISE SPENDING ANALYSIS",
        f"Month: {year}-{month:02d}",
        "",
        "Category,Amount,Percentage"
    ]
    
    for cat in categories:
        csv_lines.append(f"{cat['category']},${cat['amount']:.2f},{cat['percentage']:.1f}%")
    
    csv_content = "\n".join(csv_lines)
    return csv_content
