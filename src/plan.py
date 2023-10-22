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

def append_income(data, year, owners, social_security):
    income = 0
    for owner in owners:
        income+=owner.get_income(social_security, year)
    data.append(income)
    return income

def append_rmd(data, year, self, roth_with_rmd):
    rmd = 0
    for account in self.accounts:
        owner = get_account_owner(account, self)
        rmd += account.withdrawl_rmd(self.rmd.get_rate(owner.get_age(year)), roth_with_rmd)
    rmd = round(rmd, 2)
    data.append(rmd)
    return rmd

def append_expenses(data, year, expenses):
    value = expenses.get_expenses(year)
    data.append(value)
    return value

def append_tax(data, self, rate, rmd):
    taxable = 0
    for account in self.accounts:
        if account.is_taxable() and rate > 0:
            taxable += round((account.get_balance()) * rate/100, 2)
    tax = round(self.tax.calculate(taxable+rmd), 2)
    data.append(tax)
    return tax

def append_reinvestment(data, income, tax, expense, rmd):
    change = expense + tax - income - rmd
    
    if change < 0: data.append(-change)
    else: data.append(0.0)

    return change

def append_accounts(data, year, self, rate, change, growth):
    total = 0
    for account in self.accounts:
        retired = owner_is_retired(account, self, year)
        if growth:
            account.process_growth(rate, retired)
        if change:
            if account.withdrawl(change):
                change = 0
            else:
                balance = account.get_balance()
                change -= balance
                account.withdrawl(balance)
        balance = account.get_balance()
        data.append(balance)
        total += balance
    return round(total,2)

class Plan:
    def __init__(self, owners, accounts, expenses, rmd, tax, config):
        self.accounts = accounts
        self.owners = owners
        self.expenses = expenses
        self.rmd = rmd
        self.tax = tax
        self.config = config

    def verify_config(self):
        for account in self.accounts:
            if owner_is_not_known(account, self): return False
        return True

    def get_header(self):
        header = ["Year", "Income", "Rmd", "Expenses", "Taxes", "Reinvested"]
        for account in self.accounts:
            header.append(account.get_name())
        
        header+= ["Sum of Accounts"]
        return header

    def process_plan(self, start_year, years, rates):
        balances = []

        for i in range(years+1):
            balances.append([])
            balances[i].append(start_year+i)

            income = append_income(balances[i], start_year+i, self.owners, self.config["social_security"])
            rmd = append_rmd(balances[i], start_year+i, self, self.config["rmd"])
            expense = append_expenses(balances[i], start_year+i, self.expenses)            
            tax = append_tax(balances[i], self, rates[i], rmd)
            change = append_reinvestment(balances[i], income, tax, expense, rmd)

            total = append_accounts(balances[i], start_year+i, self, rates[i], change, i!=0)
            balances[i].append(total)

        return balances
