class Expense:
    """Class representing an expense entry"""

    def __init__(self, name, amount, category) -> None:
        """Initializes an Expense instance with name, amount, and category"""
        self.name = name
        self.amount = float(amount)
        self.category = category


    def __repr__(self) -> str:
        """Provides a string representation of the Expense instance"""
        return f"<Expense: {self.name}, {self.category}, £{self.amount:.2f} >"
