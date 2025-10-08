from collections import defaultdict
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from database import database
from utils import get_user_choice, parse_date

"""Functions for plotting graphs related to expenses and income"""

def plot_expense_summary() -> None:
    """
    Plots a summary of expenses by category using matplotlib.
    Offers the user a choice of chart types:
      1. Pie Chart (Expenses by Category %)
      2. Bar Chart (Expenses by Category £)
      3. Line Chart (Income vs Expenses over Time)
    """
    options = ['1', '2', '3']

    print("\nChoose a chart type:")
    print(" 1. Pie Chart (Expenses by Category %)")
    print(" 2. Bar Chart (Expenses by Category £)")
    print(" 3. Line Chart (Income vs Expenses over Time)")

    choice = get_user_choice("Select an option (1-3): ", options)

    summary = database.summarise_expenses()

    if not summary:
        print("No expenses to plot.")
        return

    # Pie Chart
    if choice == '1':
        categories = [category for category, total in summary]
        totals = [total for category, total in summary]

        plt.figure(figsize=(6,6))
        plt.pie(totals, labels=categories, autopct='%1.1f%%', startangle=140)  # Pie chart
        plt.title("Expenses by Category")
        plt.show()

    # Bar Chart
    elif choice == '2':
        categories = [category for category, total in summary]
        totals = [total for category, total in summary]

        plt.figure(figsize=(8,5))  # Wider figure
        plt.bar(categories, totals)
        plt.xlabel("Category")
        plt.ylabel("Total Spent (£)")
        plt.title("Expenses by Category (Bar Chart)")
        plt.show()

    # Line Chart
    elif choice == '3':
        expenses = database.get_all_expenses()
        income = database.get_all_income()

        if not expenses and not income:
            print("No income or expenses to plot.")
            return

        # Sum expenses by date
        expense_totals = defaultdict(float)
        for row in expenses:
            date, amount = parse_date(row)
            date_only = date.date()  # Only keep date
            expense_totals[date_only] += amount

        # Sum income by date
        income_totals = defaultdict(float)
        for row in income:
            date, amount = parse_date(row)
            date_only = date.date()
            income_totals[date_only] += amount

        # Get full range of dates
        all_dates = sorted(set(expense_totals.keys()) | set(income_totals.keys()))
        if all_dates:
            start_date = all_dates[0]
            end_date = all_dates[-1]
            full_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        else:
            print("No valid dates to plot.")
            return

        # Build cumulative sums
        expense_values = []
        income_values = []
        running_expense = 0
        running_income = 0

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

    else:
        print("Invalid choice. Please select 1, 2, or 3.")
