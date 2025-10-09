from datetime import datetime


def format_currency(value) -> str:
    """Formats a float as a currency string with £ and 2 decimals"""
    return f"£{value:,.2f}"

def print_formatted_entry(entry_str: str) -> None:
    """
    Takes a string and prints it with consistent formatting.
    If the string can't be parsed, prints it as-is.
    """
    try:
        prefix, rest = entry_str.strip().split(" - ")
        if rest.strip().startswith("£"):
            amount_part = rest.strip()[1:]
        else:
            amount_part = rest.strip()
        if " on " in amount_part:
            amount_str, date_str = amount_part.split(" on ")
        else:
            raise ValueError
        amount = float(amount_str.strip())
        date_str = date_str.strip(" []")
        print(f"{prefix.strip()} - {format_currency(amount)} on [{date_str}]")
    except Exception:
        print(entry_str)



def get_user_choice(prompt, options) -> str:
    """Prompts user to select an option and validates the input"""
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        else:
            print(f"Invalid choice. Please select from {', '.join(options)}.")

def get_float_input(prompt) -> float:
    """Prompts user for a float input and validates it"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_int_input(prompt) -> int:
    """Prompts user for an integer input and validates it"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

def safe_remove(func, item_id, item_name="item") -> None:
    """Tries to remove an item from the database and handles errors"""
    try:
        func(item_id)
        print(f"{item_name.capitalize()} with ID {item_id} removed.")
    except Exception as e:
        print(f"Failed to remove {item_name} with ID {item_id}: {e}")

def parse_date(entry_str: str) -> tuple[datetime, float]:
    """
    Parses an expense/income entry string and returns (datetime, amount).
    Handles extra whitespace gracefully.
    Expected format:
    'ID: Description - £Amount on [YYYY-MM-DD HH:MM:SS]'
    """
    try:
        clean_str = entry_str.strip()
        
        if " on [" not in clean_str:
            raise ValueError("Invalid entry format")
        
        date_part = clean_str.split(" on [", 1)[1]
        date_str = date_part.split("]", 1)[0].strip()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            date = datetime.strptime(date_str, "%Y-%m-%d")

        before_date = clean_str.split(" on [")[0]
        if " - £" in before_date:
            amount_str = before_date.split(" - £")[1].strip()
        elif " - " in before_date:
            amount_str = before_date.split(" - ")[1].strip()
        else:
            raise ValueError("Invalid entry format")

        amount = float(amount_str)
        return date, amount
    except Exception:
        raise ValueError("Invalid entry format")

def input_with_exit(prompt: str, exit_value='q', cast=None):
    """
    Prompts the user and allows them to exit by entering 'exit_value'
    Returns the input (cast if specified), or None if the user chooses to exit
    """
    user_input = input(f"{prompt} (or '{exit_value}' to cancel): ").strip()
    if user_input.lower() == exit_value.lower():
        return None
    if cast:
        try:
            return cast(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {cast.__name__}.")
            return input_with_exit(prompt, exit_value, cast)
    return user_input
    
