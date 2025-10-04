import sqlite3
from expense import Expense
from income import Income

# Connect to DB
expense_db = sqlite3.connect('expenses.db')
expense_cursor = expense_db.cursor()



# ----------------- TABLES -----------------


expense_cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

expense_cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP
)
""")
expense_db.commit()

# ------------ EXPENSE FUNCTIONS ------------


def add_expense(expense):
    expense_cursor.execute("""
        INSERT INTO expenses (name, category, amount) VALUES (?, ?, ?)
    """, (expense.name, expense.category, expense.amount))
    expense_db.commit()

def get_all_expenses():
    expense_cursor.execute("SELECT * FROM expenses")
    rows = expense_cursor.fetchall()
    formatted = []
    for row in rows:
        formatted.append(f"{row[0]}: {row[1]} ({row[2]}) - £{row[3]:.2f} on [{row[4]}]")
    return formatted

def remove_expense(expense_id):
    expense_cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    expense_db.commit()

def summarise_expenses():
    expense_cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    return expense_cursor.fetchall()


# ------------ INCOME FUNCTIONS ------------

def add_income(description, amount):
    expense_cursor.execute("""
        INSERT INTO income (description, amount) VALUES (?, ?)
    """, (description, amount))
    expense_db.commit()

def get_all_income():
    expense_cursor.execute("SELECT * FROM income")
    rows = expense_cursor.fetchall()
    formatted = []
    for row in rows:
        formatted.append(f"{row[0]}: {row[1]} - £{row[2]:.2f} on [{row[3]}]")
    return formatted

def remove_income(income_id):
    expense_cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
    expense_db.commit()

def get_total_income():
    expense_cursor.execute("SELECT SUM(amount) FROM income")
    total = expense_cursor.fetchone()[0]
    return total if total else 0.0




