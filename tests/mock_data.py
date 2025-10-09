from faker import Faker
import random
from datetime import datetime

fake = Faker()

CATEGORIES = ["Food", "Home", "Work", "Fun", "Misc"]

def generate_fake_expenses(n=500):
    items = []
    for i in range(1, n+1):
        name = fake.word().capitalize()
        category = random.choice(CATEGORIES)
        amount = round(random.uniform(3, 1200), 2)
        timestamp = fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S") # include time
        items.append({
            "id": i,
            "name": name,
            "category": category,
            "amount": amount,
            "date": timestamp
        })
    return items

def generate_fake_income(n=250):
    items = []
    for i in range(1, n+1):
        desc = fake.sentence(nb_words=3).rstrip('.')
        amount = round(random.uniform(50, 3000), 2)
        timestamp = fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S")
        items.append({
            "id": i,
            "description": desc,
            "amount": amount,
            "date": timestamp
        })
    return items

#simulate without touching real database
def format_expenses_for_db(expenses):
    return [
        f"{e['id']}: {e['name']} ({e['category']}) - £{e['amount']:.2f} on [{e['date']}]"
        for e in expenses
    ]

def format_income_for_db(income):
    return [
        f"{i['id']}: {i['description']} - £{i['amount']:.2f} on [{i['date']}]"
        for i in income
    ]

class MockDatabase:
    def __init__(self, ne=500, ni=250):
        self._expenses = generate_fake_expenses(ne)
        self._income = generate_fake_income(ni)

    def get_all_expenses(self):
        return format_expenses_for_db(self._expenses)

    def get_all_income(self):
        return format_income_for_db(self._income)

    def summarise_expenses(self):
        sums = {}
        for e in self._expenses:
            sums.setdefault(e["category"], 0.0)
            sums[e["category"]] += e["amount"]
        return list(sums.items())
