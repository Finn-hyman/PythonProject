import unittest
from unittest.mock import patch
from main import (
    get_expense_from_user,
    main_menu, 
    Expense, 
    remove_expense_from_user
)

"""Unit tests for main.py functions"""

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['Test Expense', '12.5', '1'])
    def test_get_expense_from_user(self, mock_input) -> None:
        """Test getting expense from user input"""
        expense = get_expense_from_user()
        self.assertIsInstance(expense, Expense)
        self.assertEqual(expense.name, 'Test Expense')
        self.assertEqual(expense.amount, 12.5)
        self.assertEqual(expense.category, 'Food')

    @patch('builtins.input', side_effect=['5', '7'])
    @patch('main.plot_expense_summary')
    def test_main_menu_plot_summary(self, mock_plot, mock_input) -> None:
        """Test going to plot expense summary in main menu"""
        main_menu()
        mock_plot.assert_called_once() # Ensure plot function was called

    @patch('builtins.input', side_effect=['1', 'Lunch', '10.0', '1', '7'])
    @patch('main.database.add_expense')
    def test_main_menu_add_expense(self, mock_add, mock_input) -> None:
        """Test adding an expense through main menu"""
        main_menu()
        mock_add.assert_called_once() # 

    @patch('builtins.input', side_effect=['2', '1', '7'])
    @patch('main.database.get_all_expenses', return_value=[Expense('Lunch', 12.5, 'Food')])
    @patch('main.database.remove_expense', return_value=True)
    def test_main_menu_remove_expense(self, mock_remove, mock_get, mock_input) -> None:
        """Test removing an expense through main menu"""
        main_menu()
        mock_remove.assert_called_once_with(1) # Verifies correct ID used

    @patch('builtins.input', side_effect=['7'])
    def test_main_menu_exit(self, mock_input) -> None:
        main_menu()

    @patch('builtins.input', side_effect=['1', 'Dinner', '15', '2', '7'])
    @patch('main.database.add_expense')
    def test_add_expense_to_db(self, mock_add, mock_input) -> None:
        """Test adding an expense to the database"""
        main_menu()
        mock_add.assert_called_once()

    @patch('builtins.input', side_effect=['1'])
    @patch('main.database.get_all_expenses', return_value=[Expense('Lunch', 12.5, 'Food')])
    @patch('main.database.remove_expense', return_value=True)
    def test_remove_expense_from_user(self, mock_remove, mock_get, mock_input) -> None:
        """Test removing an expense from user input"""
        remove_expense_from_user()
        mock_remove.assert_called_once_with(1)

    @patch('builtins.input', side_effect=['5', '7'])
    @patch('main.plot_expense_summary')
    def test_plot_expense_summary(self, mock_plot, mock_input) -> None:
        """Test plotting expense summary from main menu"""
        main_menu()
        mock_plot.assert_called_once()

if __name__ == '__main__':
    unittest.main()
