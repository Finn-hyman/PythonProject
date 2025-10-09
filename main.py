from models.expense import Expense
import csv
from models.income import Income
import database.database as database
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from collections import defaultdict
from datetime import datetime, timedelta
from graphs import plot_expense_summary
from utils import (
    format_currency, 
    print_formatted_entry, 
    get_user_choice, 
    get_float_input, 
    get_int_input, 
    safe_remove, 
    parse_date, 
    input_with_exit
)


def get_expense_from_user() -> Expense | None:
    """
    Prompts the user to input details of a new expense which includes:
    - Name
    - Amount
    - Category (chosen from a predefined list)
    
    Returns:
        Expense: An instance of the expense class with the provided details
    """
    expense_name = input_with_exit("Enter expense name", cast=str)
    if expense_name is None:
        return None

    expense_amount = input_with_exit("Enter expense amount", cast=float)
    if expense_amount is None:
        return None

    print(f"Expense name: {expense_name}, Expense amount: {expense_amount}")
    
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc"
    ]

    while True:
        print("Select a category: ")
        for i, category in enumerate(expense_categories):
            print(f"  {i + 1}. {category}")

        value_range = f"(1-{len(expense_categories)})"
        try:
            selected_index = input_with_exit(f"Enter a category number {value_range}", cast=int)
            if selected_index is None:
                return None
            selected_index -= 1
        except ValueError:
            print("Please enter a valid number.")
            continue

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print(f"Invalid input. Please enter a number {value_range}.")


def summarise_expenses() -> None:
    """
    Retrieves and prints a summary of expenses grouped by category
    """
    summary = database.summarise_expenses()
    print("\nExpense Summary:")
    for category, total in summary:
        print(f"{category}: {format_currency(total)}")

def remove_expense_from_user() -> None:
    """
    Displays all expenses and prompts the user to select one to remove by its ID
    Deleted the selected expense from the database
    """
    all_expenses = database.get_all_expenses()
    print("\nAll Expenses:")
    for exp in all_expenses:
        print_formatted_entry(exp)

    expense_id = input_with_exit("Enter the ID of the expense to remove", cast=int)
    if expense_id is None:
        print("Cancelled removing expense.")
        return

    safe_remove(database.remove_expense, expense_id, "expense")

def export_to_csv() -> None: 
    """"Exports all expenses and income to CSV files"""
    expenses = database.get_all_expenses()
    income = database.get_all_income()

    #Export expenses
    with open("expenses.csv", mode="w", newline= "", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Category", "Amount (£)", "Date"])
        for exp in expenses:
            try:
                exp_id = exp.split(":")[0].strip()
                name = exp.split(":")[1].split("(")[0].strip()
                category = exp.split("(")[1].split(")")[0].strip()
                amount = exp.split("£")[1].split("on")[0].strip()
                date = exp.split("on")[1].strip(" []")
                writer.writerow([exp_id, name, category, amount, date])
            except Exception as e:
                print(f"Failed to parse expense entry '{exp}': {e}")
            
    with open("income.csv", mode="w", newline="", encoding="utf-8") as file:
        writer =csv.writer(file)
        writer.writerow(["ID", "Description", "Amount (£)", "Date"])
        for inc in income:
            try:
                inc_id = inc.split(":")[0].strip()
                description = inc.split(":")[1].split("-")[0].strip()
                amount = inc.split("£")[1].split("on")[0].strip()
                date = inc.split("on")[1].strip(" []")
                writer.writerow([inc_id, description, amount, date])
            except Exception as e:
                print(f"Failed to parse income entry '{inc}': {e}")
        
    print("Exported expenses to 'expenses.csv' and income to 'income.csv'.")

def manage_income() -> None:
    """
    Gives a menu that allows the user to:
    - View all income entries
    - Add a new income entry
    - Remove an income entry by its ID
    """
    options = ['1', '2', '3', '4']

    while True:
        print("\nManage Income")
        print(" 1. View All Income")
        print(" 2. Add Income")
        print(" 3. Remove Income")
        print(" 4. Back to Main Menu")

        choice = get_user_choice("Select an option (1-4): ", options)
        if choice == '1':
            all_income = database.get_all_income()
            print("\nAll Income:")
            for inc in all_income:
                print_formatted_entry(inc)
            total_income = database.get_total_income()
            print(f"Total Income: {format_currency(total_income)}")
        elif choice == '2':
            description = input_with_exit("Enter income description", cast=str)
            if description is None:
                print("Cancelled adding income.")
                continue

            amount = input_with_exit("Enter income amount", cast=float)
            if amount is None:
                print("Cancelled adding income.")
                continue

            database.add_income(description, amount)
            print("Income added.")
        elif choice == '3':
            all_income = database.get_all_income()
            print("\nAll Income:")
            for inc in all_income:
                print_formatted_entry(inc)

            income_id = input_with_exit("Enter the ID of the income to remove", cast=int)
            if income_id is None:
                print("Cancelled removing income.")
                continue

            safe_remove(database.remove_income, income_id, "income")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

def main_menu() -> None:
    """
    Main menu for the Expense Tracker CLI
    """
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. View All Expenses")
        print("4. View Expense Summary by Category")
        print("5. Plot Expense Summary")
        print("6. Manage Income")
        print("7. Export Data to CSV")
        print("8. Exit")

        choice = get_user_choice("Select an option (1-8): ", [str(i) for i in range(1, 9)])

        if choice == "1":
            expense = get_expense_from_user()
            if expense is None: 
                print("Cancelled adding expense.")
                continue
            database.add_expense(expense)
            print(f"✅ Expense added: {expense.name}, £{expense.amount:.2f}, Category: {expense.category}")

        elif choice == "2":
            remove_expense_from_user()

        elif choice == "3":
            expenses = database.get_all_expenses()
            if not expenses:
                print("No expenses recorded yet.")
            else:
                print("\nAll Expenses:")
                for exp in expenses:
                    print(exp)

        elif choice == "4":
            summary = database.summarise_expenses()
            if not summary:
                print("No expenses to summarize.")
            else:
                print("\nExpense Summary by Category:")
                for category, total in summary:
                    print(f"{category}: £{total:.2f}")

        elif choice == "5":
            plot_expense_summary()

        elif choice == "6":
            manage_income()
        
        elif choice == "7":
            export_to_csv()

        elif choice == "8":
            print("Exiting the Expense Tracker. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please select a number between 1 and 8.")

def main() -> None:
    """
    Entry point for the Expense Tracker application
    """
    print(f"Running Expense Tracker!")
    main_menu()


if __name__ == "__main__":
    main()

