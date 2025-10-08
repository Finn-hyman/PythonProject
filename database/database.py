import sqlite3
from models.expense import Expense
from models.income import Income

"""Database for managing expenses and income using SQLite"""

expense_db = sqlite3.connect('expenses.db') # Connect to SQLite database 
expense_cursor = expense_db.cursor() #  Create a cursor object

expense_cursor.execute(""" 
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP
)
""") # Create expenses table if it doesn't exist

expense_cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP
)
""") # Create income table if it doesn't exist
expense_db.commit() # Commit changes


def add_expense(expense) -> None:
    """Adds a new expense to the database"""
    expense_cursor.execute("""
        INSERT INTO expenses (name, category, amount) VALUES (?, ?, ?)
    """, (expense.name, expense.category, expense.amount))
    expense_db.commit()

def get_all_expenses() -> list[str]:
    """Retrieves all expenses from the database"""
    expense_cursor.execute("SELECT * FROM expenses")
    rows = expense_cursor.fetchall()
    formatted = []
    for row in rows:
        formatted.append(f"{row[0]}: {row[1]} ({row[2]}) - £{row[3]:.2f} on [{row[4]}]")
    return formatted

def remove_expense(expense_id) -> None:
    """Removes an expense by its ID"""
    expense_cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    expense_db.commit()

def summarise_expenses() -> list[tuple[str, float]]:
    """Returns a summary of expenses grouped by category"""
    expense_cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    return expense_cursor.fetchall()


def add_income(description, amount) -> None:
    """Adds a new income entry to the database"""
    expense_cursor.execute("""
        INSERT INTO income (description, amount) VALUES (?, ?)
    """, (description, amount))
    expense_db.commit()

def get_all_income() -> list[str]:
    """Retrieves all income entries from the database"""
    expense_cursor.execute("SELECT * FROM income")
    rows = expense_cursor.fetchall()
    formatted = []
    for row in rows:
        formatted.append(f"{row[0]}: {row[1]} - £{row[2]:.2f} on [{row[3]}]")
    return formatted

def remove_income(income_id) -> None:
    """Removes an income entry by its ID"""
    expense_cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
    expense_db.commit()

def get_total_income() -> float:
    """`Returns the total income amount"""
    expense_cursor.execute("SELECT SUM(amount) FROM income")
    total = expense_cursor.fetchone()[0]
    return total if total else 0.0




