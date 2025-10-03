from expense import Expense
import database


def main():
    print(f"Running Expense Tracker!")


    # Get user to input expense
    expense = get_expense_from_user()
    print(expense)

    # Write to file
    database.add_expense(expense)
    print("Expense saved to database.")
    
    all_expenses = database.get_all_expenses()
    print("All expenses in the database:")
    for exp in all_expenses:
        print(exp)

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
                name = expense_name, category = selected_category, amount = expense_amount
            )
            return new_expense
        else:
            print(f"Invalid input. Please enter a number {value_range}.")


def summarise_expenses():
    pass


if __name__ == "__main__":
    main()