from src.account import Account
from src.owner import Owner

def owner_is_not_known(name, owners):
    for owner in owners:
        if owner.get_name() == name: return False
    return True

def append_income(data, year, owners):
    income = 0
    for owner in owners:
        income+=owner.get_income(True, year)
    data.append(income)

def process_accounts(data, year, self, growth):
    for account in self.accounts:
        if growth:
            account.process_growth(self.config["average_growth"])
        data.append(account.get_balance())

class Plan:
    def __init__(self, config, owners, accounts):
        self.config = config
        self.accounts = accounts
        self.owners = owners

    def get_growth(self):
        return self.config["average_growth"]

    def verify_config(self):
        for account in self.accounts:
            name = account.get_owner()
            if owner_is_not_known(name, self.owners): return False
        return True

    def get_header(self):
        header = ["Year", "Income"]
        for account in self.accounts:
            header.append(account.get_name())
        
        return header

    def process_growth(self, start_year, years):
        balances = []

        for i in range(years+1):
            balances.append([])
            balances[i].append(start_year+i)

            append_income(balances[i], start_year+i, self.owners)
            process_accounts(balances[i], start_year+i, self, i!=0)

        return balances
