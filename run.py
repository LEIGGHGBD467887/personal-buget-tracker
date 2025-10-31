"""
Budget Tracker Application Entry Point
"""
import os
from app import create_app

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
