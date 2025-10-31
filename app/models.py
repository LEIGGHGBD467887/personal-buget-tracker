"""
Data models and database operations for Budget Tracker
"""
import json
import os
from datetime import datetime

DATA_FILE = "budget_data.json"

class Transaction:
    """Transaction model"""
    def __init__(self, transaction_type, amount, category, description, date=None):
        self.type = transaction_type
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

class BudgetDatabase:
    """Database operations for budget tracking"""
    
    @staticmethod
    def load_data():
        """Load all transactions from file"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"transactions": []}

    @staticmethod
    def save_data(data):
        """Save transactions to file"""
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def add_transaction(transaction_type, amount, category, description, date=None):
        """Add a new transaction"""
        transaction = Transaction(transaction_type, amount, category, description, date)
        data = BudgetDatabase.load_data()
        data["transactions"].append(transaction.to_dict())
        BudgetDatabase.save_data(data)
        return transaction.to_dict()

    @staticmethod
    def get_all_transactions():
        """Get all transactions"""
        data = BudgetDatabase.load_data()
        return data.get("transactions", [])

    @staticmethod
    def delete_transaction(index):
        """Delete a transaction by index"""
        data = BudgetDatabase.load_data()
        if 0 <= index < len(data["transactions"]):
            data["transactions"].pop(index)
            BudgetDatabase.save_data(data)
            return True
        return False

    @staticmethod
    def get_transactions_by_month(year, month):
        """Get transactions for a specific month"""
        import pandas as pd
        data = BudgetDatabase.load_data()
        df = pd.DataFrame(data["transactions"])
        
        if df.empty:
            return None
        
        df['date'] = pd.to_datetime(df['date'])
        df['year_month'] = df['date'].dt.to_period('M')
        
        target_month = pd.Period(f"{year}-{month:02d}", freq='M')
        return df[df['year_month'] == target_month]
