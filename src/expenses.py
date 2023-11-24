import pandas as pd


class Expenses:
    def __init__(self, config):
        self.config = config

    def get_names(self):
        names = []
        for expense in self.config:
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


def generate_expense_over_time(expenses, start_year, years_to_process):
    expense_table = []
    for year in range(start_year, start_year+years_to_process):
        expense_table.append([year] + expenses.get_year(year))
    data = pd.DataFrame(expense_table, columns=['Year'] + expenses.get_names())

    return data
