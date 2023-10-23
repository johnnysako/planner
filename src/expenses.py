class Expenses:
    def __init__(self, config):
        self.config = config

    def get_names(self):
        names = []
        for expense in self.config:
            names.append(expense.get_name())
        return names

    def get_needs_names(self):
        names = []
        for expense in self.config:
            if expense.is_need():
                names.append(expense.get_name())
        return names

    def get_wants_names(self):
        names = []
        for expense in self.config:
            if not expense.is_need():
                names.append(expense.get_name())
        return names

    def get_expenses(self, year):
        expenses = 0
        for expense in self.config:
            expenses += expense.get_expense(year)
        return expenses

    def get_needs(self, year):
        expenses = 0
        for expense in self.config:
            if expense.is_need():
                expenses += expense.get_expense(year)
        return expenses

    def get_year(self, year):
        expenses = []
        for expense in self.config:
            expenses.append(expense.get_expense(year))
        return expenses
