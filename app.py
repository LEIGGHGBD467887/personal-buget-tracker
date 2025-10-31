from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json
from io import BytesIO
import base64

app = Flask(__name__)
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

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    data = load_data()
    df = pd.DataFrame(data["transactions"])
    if df.empty:
        return jsonify({"transactions": []})
    df = df.sort_values('date', ascending=False)
    return jsonify({"transactions": df.to_dict('records')})

@app.route('/api/add-transaction', methods=['POST'])
def add_transaction():
    """Add a new transaction"""
    try:
        req_data = request.json
        data = load_data()
        transaction = {
            "type": req_data['type'],
            "amount": float(req_data['amount']),
            "category": req_data['category'],
            "description": req_data['description'],
            "date": req_data['date']
        }
        data["transactions"].append(transaction)
        save_data(data)
        return jsonify({"success": True, "message": "Transaction added successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/monthly-report/<int:year>/<int:month>', methods=['GET'])
def monthly_report(year, month):
    """Get monthly report"""
    data = load_data()
    df = pd.DataFrame(data["transactions"])
    
    if df.empty:
        return jsonify({"error": "No transactions found"}), 404
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    target_month = pd.Period(f"{year}-{month:02d}", freq='M')
    monthly_data = df[df['year_month'] == target_month]
    
    if monthly_data.empty:
        return jsonify({"error": f"No transactions found for {year}-{month:02d}"}), 404
    
    income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
    expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
    balance = income - expenses
    
    return jsonify({
        "year": year,
        "month": month,
        "income": float(income),
        "expenses": float(expenses),
        "balance": float(balance)
    })

@app.route('/api/category-analysis/<int:year>/<int:month>', methods=['GET'])
def category_analysis(year, month):
    """Get category-wise spending analysis"""
    data = load_data()
    df = pd.DataFrame(data["transactions"])
    
    if df.empty:
        return jsonify({"error": "No transactions found"}), 404
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    target_month = pd.Period(f"{year}-{month:02d}", freq='M')
    monthly_data = df[df['year_month'] == target_month]
    
    if monthly_data.empty:
        return jsonify({"error": f"No transactions found for {year}-{month:02d}"}), 404
    
    expenses = monthly_data[monthly_data['type'] == 'expense']
    
    if expenses.empty:
        return jsonify({"categories": []})
    
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
    
    return jsonify({"categories": categories})

@app.route('/api/chart/category/<int:year>/<int:month>', methods=['GET'])
def chart_category(year, month):
    """Generate category pie chart"""
    data = load_data()
    df = pd.DataFrame(data["transactions"])
    
    if df.empty:
        return jsonify({"error": "No transactions found"}), 404
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    target_month = pd.Period(f"{year}-{month:02d}", freq='M')
    monthly_data = df[df['year_month'] == target_month]
    
    expenses = monthly_data[monthly_data['type'] == 'expense']
    
    if expenses.empty:
        return jsonify({"error": "No expenses found"}), 404
    
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
    return jsonify({"image": f"data:image/png;base64,{img_base64}"})

@app.route('/api/chart/income-vs-expense/<int:year>/<int:month>', methods=['GET'])
def chart_income_vs_expense(year, month):
    """Generate income vs expense bar chart"""
    data = load_data()
    df = pd.DataFrame(data["transactions"])
    
    if df.empty:
        return jsonify({"error": "No transactions found"}), 404
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    target_month = pd.Period(f"{year}-{month:02d}", freq='M')
    monthly_data = df[df['year_month'] == target_month]
    
    if monthly_data.empty:
        return jsonify({"error": "No transactions found"}), 404
    
    income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
    expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
    
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
    return jsonify({"image": f"data:image/png;base64,{img_base64}"})

@app.route('/api/delete-transaction/<int:index>', methods=['DELETE'])
def delete_transaction(index):
    """Delete a transaction"""
    try:
        data = load_data()
        if 0 <= index < len(data["transactions"]):
            data["transactions"].pop(index)
            save_data(data)
            return jsonify({"success": True, "message": "Transaction deleted"})
        return jsonify({"success": False, "message": "Invalid index"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
