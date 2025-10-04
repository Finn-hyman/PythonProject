class Income:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

    def __repr__(self):
        return f"Income(description={self.description}, amount={self.amount})"