import sqlite3
from expense import Expense

# All SQL here

expense_db = sqlite3.connect('expenses.db')
expense_cursor = expense_db.cursor()

# Create table
expense_cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

expense_db.commit()

def add_expense(expense):
    expense_cursor.execute("""
        INSERT INTO expenses (name, category, amount) VALUES (?, ?, ?)
    """, (expense.name, expense.category, expense.amount))
    expense_db.commit()


def get_all_expenses():
    expense_cursor.execute("SELECT * FROM expenses")
    return expense_cursor.fetchall()
