// Budget Tracker Main JavaScript

// Set today's date as default
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('date').valueAsDate = new Date();

    // Set current year and month as default
    const now = new Date();
    document.getElementById('reportYear').value = now.getFullYear();
    document.getElementById('reportMonth').value = now.getMonth() + 1;
    document.getElementById('analysisYear').value = now.getFullYear();
    document.getElementById('analysisMonth').value = now.getMonth() + 1;
    document.getElementById('chartYear').value = now.getFullYear();
    document.getElementById('chartMonth').value = now.getMonth() + 1;

    // Load dashboard and budget alert on page load
    loadDashboard();
    checkBudgetAlert();
});

function showMessage(message, type) {
    const msgEl = document.getElementById('message');
    msgEl.textContent = message;
    msgEl.className = `message ${type}`;
    setTimeout(() => {
        msgEl.className = 'message';
    }, 3000);
}

function checkBudgetAlert() {
    fetch('/api/budget-alert')
    .then(res => res.json())
    .then(data => {
        const alertContainer = document.getElementById('budgetAlertContainer');
        if (!alertContainer) return;

        if (data.alert) {
            // Expenses exceed income - show warning
            alertContainer.innerHTML = `
                <div class="alert-box danger">
                    <strong>⚠️ BUDGET ALERT!</strong><br>
                    ${data.message}
                </div>
            `;
        } else if (data.message) {
            // Good financial status
            alertContainer.innerHTML = `
                <div class="alert-box success">
                    ${data.message}
                </div>
            `;
        }
    })
    .catch(err => console.error('Error checking budget alert:', err));
}

function addTransaction() {
    const type = document.getElementById('transactionType').value;
    const amount = document.getElementById('amount').value;
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;
    const date = document.getElementById('date').value;

    if (!amount || !category || !description || !date) {
        showMessage('Please fill all fields', 'error');
        return;
    }

    fetch('/api/add-transaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, amount, category, description, date })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showMessage('Transaction added successfully!', 'success');
            document.getElementById('amount').value = '';
            document.getElementById('category').value = '';
            document.getElementById('description').value = '';
            document.getElementById('date').valueAsDate = new Date();
            loadTransactions();
            loadDashboard();
            checkBudgetAlert();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(err => showMessage('Error: ' + err, 'error'));
}

function loadTransactions() {
    fetch('/api/transactions')
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('transactionsContainer');
        if (data.transactions.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No transactions yet. Add one to get started!</p></div>';
            return;
        }

        let html = '<table class="transactions-table"><thead><tr><th>Date</th><th>Type</th><th>Category</th><th>Description</th><th>Amount</th><th>Action</th></tr></thead><tbody>';
        data.transactions.forEach((t, idx) => {
            const badge = `<span class="badge ${t.type}">${t.type.toUpperCase()}</span>`;
            html += `<tr>
                <td>${t.date}</td>
                <td>${badge}</td>
                <td>${t.category}</td>
                <td>${t.description}</td>
                <td>$${parseFloat(t.amount).toFixed(2)}</td>
                <td><button class="delete-btn" onclick="deleteTransaction(${idx})">Delete</button></td>
            </tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    })
    .catch(err => console.error('Error:', err));
}

function deleteTransaction(index) {
    if (confirm('Are you sure you want to delete this transaction?')) {
        fetch(`/api/delete-transaction/${index}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showMessage('Transaction deleted', 'success');
                loadTransactions();
                loadDashboard();
                checkBudgetAlert();
            }
        })
        .catch(err => console.error('Error:', err));
    }
}

function getMonthlyReport() {
    const year = document.getElementById('reportYear').value;
    const month = document.getElementById('reportMonth').value;

    if (!year || !month) {
        showMessage('Please select year and month', 'error');
        return;
    }

    fetch(`/api/monthly-report/${year}/${month}`)
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'error');
            document.getElementById('reportStats').style.display = 'none';
        } else {
            document.getElementById('reportIncome').textContent = `$${data.income.toFixed(2)}`;
            document.getElementById('reportExpenses').textContent = `$${data.expenses.toFixed(2)}`;
            document.getElementById('reportBalance').textContent = `$${data.balance.toFixed(2)}`;
            document.getElementById('reportStats').style.display = 'grid';
        }
    })
    .catch(err => showMessage('Error: ' + err, 'error'));
}

function getCategoryAnalysis() {
    const year = document.getElementById('analysisYear').value;
    const month = document.getElementById('analysisMonth').value;

    if (!year || !month) {
        showMessage('Please select year and month', 'error');
        return;
    }

    fetch(`/api/category-analysis/${year}/${month}`)
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('analysisContainer');
        if (data.error) {
            container.innerHTML = `<div class="empty-state"><p>${data.error}</p></div>`;
        } else if (data.categories.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No expenses found for this month</p></div>';
        } else {
            let html = '<table class="transactions-table"><thead><tr><th>Category</th><th>Amount</th><th>Percentage</th></tr></thead><tbody>';
            data.categories.forEach(cat => {
                html += `<tr>
                    <td>${cat.category}</td>
                    <td>$${cat.amount.toFixed(2)}</td>
                    <td>${cat.percentage.toFixed(1)}%</td>
                </tr>`;
            });
            html += '</tbody></table>';
            container.innerHTML = html;
        }
    })
    .catch(err => console.error('Error:', err));
}

function getChart(type) {
    const year = document.getElementById('chartYear').value;
    const month = document.getElementById('chartMonth').value;

    if (!year || !month) {
        showMessage('Please select year and month', 'error');
        return;
    }

    const endpoint = type === 'category' ? 
        `/api/chart/category/${year}/${month}` : 
        `/api/chart/income-vs-expense/${year}/${month}`;

    fetch(endpoint)
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('chartsContainer');
        if (data.error) {
            container.innerHTML = `<div class="empty-state"><p>${data.error}</p></div>`;
        } else {
            container.innerHTML = `<div class="chart-container"><img src="${data.image}" alt="Chart"></div>`;
        }
    })
    .catch(err => console.error('Error:', err));
}

function loadDashboard() {
    fetch('/api/transactions')
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('dashboardContainer');
        if (data.transactions.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No transactions yet. Start by adding your first transaction!</p></div>';
            return;
        }

        let totalIncome = 0, totalExpense = 0;
        const categorySpending = {};
        
        data.transactions.forEach(t => {
            if (t.type === 'income') {
                totalIncome += parseFloat(t.amount);
            } else {
                totalExpense += parseFloat(t.amount);
                categorySpending[t.category] = (categorySpending[t.category] || 0) + parseFloat(t.amount);
            }
        });

        let html = `
            <div class="stats-grid">
                <div class="stat-box">
                    <h3>Total Income</h3>
                    <div class="amount">$${totalIncome.toFixed(2)}</div>
                </div>
                <div class="stat-box">
                    <h3>Total Expenses</h3>
                    <div class="amount">$${totalExpense.toFixed(2)}</div>
                </div>
                <div class="stat-box">
                    <h3>Balance</h3>
                    <div class="amount">$${(totalIncome - totalExpense).toFixed(2)}</div>
                </div>
            </div>
            <h3 style="margin-top: 30px; margin-bottom: 15px; color: #2c3e50;">Top Spending Categories</h3>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Amount</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
        `;

        const sortedCategories = Object.entries(categorySpending)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);

        sortedCategories.forEach(([cat, amount]) => {
            const percentage = (amount / totalExpense) * 100;
            html += `<tr>
                <td>${cat}</td>
                <td>$${amount.toFixed(2)}</td>
                <td>${percentage.toFixed(1)}%</td>
            </tr>`;
        });

        html += '</tbody></table>';
        container.innerHTML = html;
    })
    .catch(err => console.error('Error:', err));
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    if (event && event.target) {
        event.target.classList.add('active');
    }

    // Load data based on tab
    if (tabName === 'transactions') {
        loadTransactions();
    } else if (tabName === 'dashboard') {
        loadDashboard();
    }
}

function exportAllTransactionsCSV() {
    window.location.href = '/api/export/all-transactions';
}

function exportMonthlyReportCSV() {
    const year = document.getElementById('reportYear').value;
    const month = document.getElementById('reportMonth').value;

    if (!year || !month) {
        showMessage('Please select year and month', 'error');
        return;
    }

    window.location.href = `/api/export/monthly-report/${year}/${month}`;
}

function exportCategoryAnalysisCSV() {
    const year = document.getElementById('analysisYear').value;
    const month = document.getElementById('analysisMonth').value;

    if (!year || !month) {
        showMessage('Please select year and month', 'error');
        return;
    }

    window.location.href = `/api/export/category-analysis/${year}/${month}`;
}
