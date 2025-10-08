from collections import defaultdict
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from database import database
from utils import get_user_choice, parse_date, input_with_exit

"""Functions for plotting graphs related to expenses and income"""

def plot_expense_summary() -> None:
    """
    Plots a summary of expenses by category using matplotlib.
    Offers the user a choice of chart types:
      1. Pie Chart (Expenses by Category %)
      2. Bar Chart (Expenses by Category £)
      3. Line Chart (Income vs Expenses over Time)
    """
    print("\nChoose a chart type:")
    print(" 1. Pie Chart (Expenses by Category %)")
    print(" 2. Bar Chart (Expenses by Category £)")
    print(" 3. Line Chart (Income vs Expenses over Time)")

    choice = input_with_exit("Select a chart type (1-3)", cast=int)
    if choice is None:
        print("Cancelled plotting.")
        return
    if choice not in [1, 2, 3]:
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    summary = database.summarise_expenses()
    if not summary and choice in [1, 2]:
        print("No expenses to plot.")
        return

    categories = [category for category, total in summary]
    totals = [total for category, total in summary]

    # Pie Chart
    if choice == 1:
        plt.figure(figsize=(6,6))
        plt.pie(totals, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Expenses by Category")
        plt.show()

    # Bar Chart
    elif choice == 2:
        plt.figure(figsize=(8,5))
        plt.bar(categories, totals)
        plt.xlabel("Category")
        plt.ylabel("Total Spent (£)")
        plt.title("Expenses by Category (Bar Chart)")
        plt.show()

    # Line Chart
    elif choice == 3:
        expenses = database.get_all_expenses()
        income = database.get_all_income()
        if not expenses and not income:
            print("No income or expenses to plot.")
            return
    
        def sum_by_date(rows):
            totals = defaultdict(float)
            for row in rows:
                date, amount = parse_date(row)
                totals[date.date()] += amount
            return totals
        
        expense_totals = sum_by_date(expenses)
        income_totals = sum_by_date(income)

        # Full date range
        all_dates = sorted(set(expense_totals) | set(income_totals))
        if not all_dates:
            print("No valid dates to plot.")
            return
        start, end = all_dates[0], all_dates[-1]
        full_range = [start + timedelta(days=i) for i in range((end - start).days + 1)]

        # Cumulative sums
        expense_values, income_values = [], []
        running_expense = running_income = 0
        for d in full_range:
            running_expense += expense_totals.get(d, 0)
            running_income += income_totals.get(d, 0)
            expense_values.append(running_expense)
            income_values.append(running_income)

        # Plot line chart
        plt.figure(figsize=(10,5))
        plt.plot(full_range, expense_values, label="Expenses", marker='o', color='tab:blue')
        plt.plot(full_range, income_values, label="Income", marker='s', color='tab:orange')
        plt.xlabel("Date")
        plt.ylabel("Amount (£)")
        plt.title("Income vs Expenses Over Time")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
