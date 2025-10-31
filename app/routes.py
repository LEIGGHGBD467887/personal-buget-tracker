"""
API routes for Budget Tracker
"""
from flask import Blueprint, render_template, request, jsonify, send_file
from app.models import BudgetDatabase
from app.utils import (
    get_monthly_summary,
    get_category_analysis,
    generate_category_chart,
    generate_income_vs_expense_chart,
    check_budget_alert,
    export_all_transactions_csv,
    export_monthly_report_csv,
    export_category_analysis_csv
)
from io import BytesIO
from datetime import datetime

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
main_bp = Blueprint('main', __name__)

# Main Routes
@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# API Routes
@api_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    transactions = BudgetDatabase.get_all_transactions()
    # Sort by date descending
    transactions.sort(key=lambda x: x['date'], reverse=True)
    return jsonify({"transactions": transactions})

@api_bp.route('/add-transaction', methods=['POST'])
def add_transaction():
    """Add a new transaction"""
    try:
        data = request.json
        transaction = BudgetDatabase.add_transaction(
            data['type'],
            data['amount'],
            data['category'],
            data['description'],
            data.get('date')
        )
        return jsonify({"success": True, "message": "Transaction added successfully", "data": transaction})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@api_bp.route('/delete-transaction/<int:index>', methods=['DELETE'])
def delete_transaction(index):
    """Delete a transaction"""
    try:
        if BudgetDatabase.delete_transaction(index):
            return jsonify({"success": True, "message": "Transaction deleted"})
        return jsonify({"success": False, "message": "Invalid index"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@api_bp.route('/monthly-report/<int:year>/<int:month>', methods=['GET'])
def monthly_report(year, month):
    """Get monthly report"""
    summary = get_monthly_summary(year, month)
    if summary is None:
        return jsonify({"error": f"No transactions found for {year}-{month:02d}"}), 404
    
    return jsonify({
        "year": year,
        "month": month,
        "income": summary['income'],
        "expenses": summary['expenses'],
        "balance": summary['balance']
    })

@api_bp.route('/category-analysis/<int:year>/<int:month>', methods=['GET'])
def category_analysis(year, month):
    """Get category-wise spending analysis"""
    categories = get_category_analysis(year, month)
    if categories is None:
        return jsonify({"error": f"No transactions found for {year}-{month:02d}"}), 404
    
    return jsonify({"categories": categories})

@api_bp.route('/chart/category/<int:year>/<int:month>', methods=['GET'])
def chart_category(year, month):
    """Generate category pie chart"""
    image = generate_category_chart(year, month)
    if image is None:
        return jsonify({"error": "No expenses found"}), 404
    
    return jsonify({"image": image})

@api_bp.route('/chart/income-vs-expense/<int:year>/<int:month>', methods=['GET'])
def chart_income_vs_expense(year, month):
    """Generate income vs expense bar chart"""
    image = generate_income_vs_expense_chart(year, month)
    if image is None:
        return jsonify({"error": "No transactions found"}), 404
    
    return jsonify({"image": image})

@api_bp.route('/budget-alert', methods=['GET'])
def budget_alert():
    """Check budget status and return alert if expenses exceed income"""
    alert_data = check_budget_alert()
    return jsonify(alert_data)

@api_bp.route('/export/all-transactions', methods=['GET'])
def export_all_transactions():
    """Export all transactions as CSV"""
    csv_content = export_all_transactions_csv()
    if csv_content is None:
        return jsonify({"error": "No transactions to export"}), 404
    
    # Create file-like object
    csv_file = BytesIO(csv_content.encode('utf-8'))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"budget_transactions_{timestamp}.csv"
    
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@api_bp.route('/export/monthly-report/<int:year>/<int:month>', methods=['GET'])
def export_monthly_report(year, month):
    """Export monthly report as CSV"""
    csv_content = export_monthly_report_csv(year, month)
    if csv_content is None:
        return jsonify({"error": f"No data for {year}-{month:02d}"}), 404
    
    # Create file-like object
    csv_file = BytesIO(csv_content.encode('utf-8'))
    filename = f"budget_report_{year}_{month:02d}.csv"
    
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@api_bp.route('/export/category-analysis/<int:year>/<int:month>', methods=['GET'])
def export_category_analysis(year, month):
    """Export category analysis as CSV"""
    csv_content = export_category_analysis_csv(year, month)
    if csv_content is None:
        return jsonify({"error": f"No data for {year}-{month:02d}"}), 404
    
    # Create file-like object
    csv_file = BytesIO(csv_content.encode('utf-8'))
    filename = f"budget_category_analysis_{year}_{month:02d}.csv"
    
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )
