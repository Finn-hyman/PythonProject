from tests.mock_data import MockDatabase
import database.database as db
import graphs
from unittest.mock import patch
import matplotlib.pyplot as plt

mock_db = MockDatabase(ne=500, ni=250)

db.get_all_expenses = mock_db.get_all_expenses
db.get_all_income = mock_db.get_all_income
db.summarise_expenses = mock_db.summarise_expenses

plt.show = plt.show  


graphs.plot_expense_summary()
