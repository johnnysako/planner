from src.account import Account
from src.owner import Owner
from src.expenses import Expenses

def owner_is_not_known(name, owners):
    for owner in owners:
        if owner.get_name() == name: return False
    return True

def append_income(data, year, owners):
    income = 0
    for owner in owners:
        income+=owner.get_income(True, year)
    data.append(income)

def owner_is_retired(owner_name, self, year):
    for owner in self.owners:
        if owner.get_name() == owner_name:
            return owner.is_retired(year)
    return False

def process_accounts(data, year, self, growth):
    for account in self.accounts:
        retired = owner_is_retired(account.get_owner(), self, year)
        if growth:
            account.process_growth(self.config["average_growth"], retired)
        data.append(account.get_balance())

def append_expenses(data, year, expenses):
    data.append(expenses.get_expenses(year))        

class Plan:
    def __init__(self, config, owners, accounts, expenses):
        self.config = config
        self.accounts = accounts
        self.owners = owners
        self.expenses = expenses

    def get_growth(self):
        return self.config["average_growth"]

    def verify_config(self):
        for account in self.accounts:
            name = account.get_owner()
            if owner_is_not_known(name, self.owners): return False
        return True

    def get_header(self):
        header = ["Year", "Income", "Expenses"]
        for account in self.accounts:
            header.append(account.get_name())
        
        return header

    def process_growth(self, start_year, years):
        balances = []

        for i in range(years+1):
            balances.append([])
            balances[i].append(start_year+i)

            append_income(balances[i], start_year+i, self.owners)
            append_expenses(balances[i], start_year+i, self.expenses)
            process_accounts(balances[i], start_year+i, self, i!=0)

        return balances
