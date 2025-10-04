from expense import Expense
from income import Income
import database
import matplotlib.pyplot as plt


# ------------------------------
# Helper Functions
# ------------------------------

def get_expense_from_user():
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
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
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
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


def summarise_expenses():
    summary = database.summarise_expenses()
    print("\nExpense Summary:")
    for category, total in summary:
        print(f"{category}: £{total:.2f}")


def remove_expense_from_user():
    all_expenses = database.get_all_expenses()
    print("\nAll Expenses:")
    for exp in all_expenses:
        print(" ", exp)
    
    try:
        expense_id = int(input("Enter the ID of the expense to remove: "))
        database.remove_expense(expense_id)
        print(f"Expense with ID {expense_id} removed.")
    except ValueError:
        print("Please enter a valid number.")


def manage_income():
    while True:
        print("\n Manage Income")
        print(" 1. View All Income")
        print(" 2. Add Income")
        print(" 3. Remove Income")
        print(" 4. Back to Main Menu")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            all_income = database.get_all_income()
            print("\nAll Income:")
            for inc in all_income:
                print(" ", inc)
            print(f"Total Income: £{database.get_total_income():.2f}")
        
        elif choice == '2':
            description = input("Enter income description: ")
            try:
                amount = float(input("Enter income amount: "))
                database.add_income(description, amount)
                print("Income added.")
            except ValueError:
                print("Please enter a valid number.")
            
        elif choice == '3':
            all_income = database.get_all_income()
            print("\nAll Income:")
            for inc in all_income:
                print(" ", inc)
            try:
                income_id = int(input("Enter the ID of the income to remove: "))
                database.remove_income(income_id)
                print(f"Income with ID {income_id} removed.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")


# ------------------------------
# Main Menu
# ------------------------------

def main_menu():
    while True:
        print("\n Main Menu")
        print(" 1. Add Expense")
        print(" 2. Remove Expense")
        print(" 3. View All Expenses")
        print(" 4. View Expense Summary by Category")
        print(" 5. Plot Expense Summary")
        print(" 6. Manage Income")
        print(" 7. Exit")

        choice = input("Select an option (1-7): ")

        if choice == '1':
            expense = get_expense_from_user()
            database.add_expense(expense)
            print("Expense saved to database.")
        elif choice == '2':
            remove_expense_from_user()
        elif choice == '3':
            all_expenses = database.get_all_expenses()
            print("\nAll Expenses:")
            for exp in all_expenses:
                print(" ", exp)
        elif choice == '4':
            summarise_expenses()
        elif choice == '5':
            plot_expense_summary()
        elif choice == '6':
            manage_income()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


# ------------------------------
# Main Program Entry
# ------------------------------

def main():
    print(f"Running Expense Tracker!")
    main_menu()


if __name__ == "__main__":
    main()