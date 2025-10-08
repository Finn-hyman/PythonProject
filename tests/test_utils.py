import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils import (
    format_currency,
    print_formatted_entry,
    get_user_choice,
    get_float_input,
    get_int_input,
    safe_remove,
    parse_date
)

"""Unit tests for utils.py functions"""

class TestUtils(unittest.TestCase):

    def test_format_currency(self) -> None:
        """Test currency formatting"""
        self.assertEqual(format_currency(1234.5), "£1,234.50") # Standard case
        self.assertEqual(format_currency(0), "£0.00") # Zero case
        self.assertEqual(format_currency(1000000), "£1,000,000.00") # Large number

    @patch("builtins.print")
    def test_print_formatted_entry_valid(self, mock_print) -> None:
        """Test printing a well-formatted entry"""
        entry = "1: Lunch (Food) - £12.5 on [2023-10-01]" 
        print_formatted_entry(entry)
        mock_print.assert_called_with("1: Lunch (Food) - £12.50 on [2023-10-01]")

    @patch("builtins.print")
    def test_print_formatted_entry_whitespace(self, mock_print) -> None:
        """Test printing an entry with extra whitespace"""
        entry = "  2: Coffee (Drink) -  £3.2 on [2023-10-02 ]  " 
        print_formatted_entry(entry)
        mock_print.assert_called_with("2: Coffee (Drink) - £3.20 on [2023-10-02]")

    @patch("builtins.print")
    def test_print_formatted_entry_invalid(self, mock_print) -> None:
        """Test printing an invalid entry""" 
        entry = "This line is invalid"
        print_formatted_entry(entry)
        mock_print.assert_called_with("This line is invalid")

    @patch("builtins.input", side_effect=["x", "b"])
    @patch("builtins.print")
    def test_get_user_choice(self, mock_print, mock_input) -> None:
        """Test user choice input and validation"""
        result = get_user_choice("Choose: ", ["a", "b"]) 
        self.assertEqual(result, "b")
        mock_print.assert_called_with("Invalid choice. Please select from a, b.")

    @patch("builtins.input", side_effect=["abc", "12.3"])
    @patch("builtins.print")
    def test_get_float_input(self, mock_print, mock_input) -> None:
        """Test float input and validation"""
        result = get_float_input("Enter number: ")
        self.assertEqual(result, 12.3)
        mock_print.assert_called_with("Please enter a valid number.")

    @patch("builtins.input", side_effect=["abc", "5"])
    @patch("builtins.print")
    def test_get_int_input(self, mock_print, mock_input) -> None:
        """Test integer input and validation"""
        result = get_int_input("Enter integer: ")
        self.assertEqual(result, 5)
        mock_print.assert_called_with("Please enter a valid integer.")

    @patch("builtins.print")
    def test_safe_remove_success(self, mock_print) -> None:
        """Test safe removal function on success"""
        func = MagicMock()
        safe_remove(func, 1, "expense")
        mock_print.assert_called_with("Expense with ID 1 removed.")
        func.assert_called_with(1)

    @patch("builtins.print")
    def test_safe_remove_failure(self, mock_print) -> None:
        """Test safe removal function on failure"""
        def faulty_func(x): raise Exception("Database error")
        safe_remove(faulty_func, 99, "income")
        mock_print.assert_called_with("Failed to remove income with ID 99: Database error")

    def test_parse_date_valid(self) -> None:
        """Test parsing date and amount from entry string"""
        entry = "1: Lunch (Food) - £12.50 on [2023-10-01]"
        date, amount = parse_date(entry)
        self.assertEqual(date, datetime(2023, 10, 1))
        self.assertEqual(amount, 12.5)

    def test_parse_date_alt_format(self) -> None:
        """Test parsing date and amount without £ symbol"""
        entry = "2: Coffee (Drink) - 3.20 on [2023-10-02]"
        date, amount = parse_date(entry)
        self.assertEqual(date, datetime(2023, 10, 2))
        self.assertEqual(amount, 3.20)

    def test_parse_date_whitespace(self) -> None:
        """Test parsing date and amount with extra whitespace"""
        entry = " 3: Snack - £4.00 on [2023-10-03 ] "
        date, amount = parse_date(entry)
        self.assertEqual(date, datetime(2023, 10, 3))
        self.assertEqual(amount, 4.00)

    def test_parse_date_invalid(self) -> None:
        """Test parsing an invalid entry string"""
        with self.assertRaises(ValueError):
            parse_date("Not a valid entry")

    def test_parse_date_missing_date(self) -> None:
        """Test parsing an entry string missing date part"""
        with self.assertRaises(ValueError):
            parse_date("1: Something - £2.00 no date")


if __name__ == "__main__":
    unittest.main()
