from src.account import Account
from src.owner import Owner
from src.expenses import Expenses

def get_account_owner(account, self):
    owner_name = account.get_owner()
    for owner in self.owners:
        if owner.get_name() == owner_name:
            return owner

def owner_is_not_known(account, self):
    owner = get_account_owner(account, self)
    for o in self.owners:
        if o == owner: return False
    return True

def owner_is_retired(account, self, year):
    owner = get_account_owner(account, self)
    return owner.is_retired(year)

def append_income(data, year, owners):
    income = 0
    for owner in owners:
        income+=owner.get_income(True, year)
    data.append(income)

def append_rmd(data, year, self):
    rmd = 0
    for account in self.accounts:
        owner = get_account_owner(account, self)
        rmd += account.withdrawl_rmd(self.rmd.get_rate(owner.get_age(year)))
    data.append(rmd)
    return rmd

def append_expenses(data, year, expenses):
    data.append(expenses.get_expenses(year))        

def append_tax(data, self, rmd):
    taxable = 0
    for account in self.accounts:
        if account.is_taxable():
            taxable += round(account.get_balance() * self.config["average_growth"]/100, 2)
    data.append(round(self.tax.calculate(taxable+rmd),2))

def append_accounts(data, year, self, growth):
    for account in self.accounts:
        retired = owner_is_retired(account, self, year)
        if growth:
            account.process_growth(self.config["average_growth"], retired)
        data.append(account.get_balance())

class Plan:
    def __init__(self, config, owners, accounts, expenses, rmd, tax):
        self.config = config
        self.accounts = accounts
        self.owners = owners
        self.expenses = expenses
        self.rmd = rmd
        self.tax = tax

    def get_growth(self):
        return self.config["average_growth"]

    def verify_config(self):
        for account in self.accounts:
            if owner_is_not_known(account, self): return False
        return True

    def get_header(self):
        header = ["Year", "Income", "Rmd", "Expenses"]
        for account in self.accounts:
            header.append(account.get_name())
        
        header.append("Taxes")
        return header

    def process_growth(self, start_year, years):
        balances = []

        for i in range(years+1):
            balances.append([])
            balances[i].append(start_year+i)

            append_income(balances[i], start_year+i, self.owners)
            rmd = append_rmd(balances[i], start_year+i, self)
            append_expenses(balances[i], start_year+i, self.expenses)
            append_accounts(balances[i], start_year+i, self, i!=0)
            append_tax(balances[i], self, rmd)

        return balances
