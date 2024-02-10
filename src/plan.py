class Plan:
    def __init__(self, start_year, owners, accounts, expenses, rmd, tax, config):
        self.start_year = start_year
        self.accounts = accounts
        self.owners = owners
        self.expenses = expenses
        self.rmd = rmd
        self.tax = tax
        self.config = config
        self.balances = []

    def _get_account_owner(self, account):
        owner_name = account.get_owner()
        return next((owner for owner in self.owners
                     if owner.get_name() == owner_name), None)

    def _owner_is_not_known(self, account):
        owner = self._get_account_owner(account)
        return not any(o == owner for o in self.owners)

    def _owner_is_retired(self, account, year):
        owner = self._get_account_owner(account)
        return owner.is_retired(year)

    def _all_owners_retired(self, year):
        return all(o.is_retired(year) for o in self.owners)

    def _append_income(self, i, year):
        income = 0
        for owner in self.owners:
            income += owner.get_income(self.config["Social Security"], year)
        self.balances[i].append(income)
        return income

    def _append_rmd(self, i, year):
        rmd = 0
        for account in self.accounts:
            owner = self._get_account_owner(account)
            rmd += account.withdraw_rmd(self.rmd.get_rate(
                owner.get_age(year)), self.config['rmd'])
        rmd = round(rmd, 2)
        self.balances[i].append(rmd)
        return rmd

    def _append_expenses(self, i, year, ):
        value = self.expenses.get_expenses(year)
        self.balances[i].append(value)
        return value

    def _calculate_tax(self, year, rate, rmd):
        taxable_growth = 0
        for account in self.accounts:
            growth = account.get_growth(year, rate)
            if account.is_taxable() and growth > 0:
                taxable_growth += round(growth, 2)
        if self._all_owners_retired(year):
            return round(self.tax.calculate(taxable_growth + rmd), 2)
        else:
            return 0

    def _append_tax(self, i, year, rate, rmd):
        tax = self._calculate_tax(year, rate, rmd)
        self.balances[i].append(tax)
        return tax

    def _append_reinvestment(self, i, income, tax, expense, rmd, year):
        change = expense + tax - income - rmd

        if change < 0 and self._all_owners_retired(year):
            change = 0.0

        self.balances[i].append(max(-change, 0.0))
        return change

    def _append_accounts(self, i, year, rate, change, growth):
        total = 0
        for account in self.accounts:
            retired = self._owner_is_retired(account, year)
            if growth:
                account.process_growth(year, rate, retired)

            if change:
                if account.withdraw(change):
                    change = 0
                else:
                    balance = account.get_balance()
                    change -= balance
                    account.withdraw(balance)
            balance = account.get_balance()
            self.balances[i].append(balance)
            total += balance
        return round(total, 2)

    def _append_rates(self, i, rates, year):
        if self._bad_timing(year):
            rates["s"][i] = -37
            rates["b"][i] = 13.4

        self.balances[i].append(rates["s"][i])
        self.balances[i].append(rates["b"][i])

        return {"s": rates["s"][i], "b": rates["b"][i]}

    def _append_percent_pulled(self, i, change, total):
        if change > 0 and total > 0:
            self.balances[i].append(round(change/total*100, 2))
        else:
            self.balances[i].append(0.0)
        self.balances[i].append(total)

    def _bad_timing(self, year):
        retirement_year = 65535
        for owner in self.owners:
            if owner.retired_year() < retirement_year:
                retirement_year = owner.retired_year()

        return year == retirement_year and self.config["bad_timing"]

    def verify_config(self):
        for account in self.accounts:
            if self._owner_is_not_known(account):
                return False
        return True

    def get_header(self):
        header = ['Year', 'Stock Returns', 'Bond Returns', 'Income', 'Rmd',
                  'Expenses', 'Taxes', 'Reinvested']
        for account in self.accounts:
            header.append(account.get_name())

        header += ['% Withdrawn', 'Sum of Accounts']
        return header

    def process_plan(self, years, rates):

        for plan_iteration, year in enumerate(range(self.start_year, 
                                       self.start_year + years + 1)):
            self.balances.append([])
            self.balances[plan_iteration].append(year)

            rate = self._append_rates(plan_iteration, rates, year)
            income = self._append_income(plan_iteration, year)
            rmd = self._append_rmd(plan_iteration, year)
            expense = self._append_expenses(plan_iteration, year)
            tax = self._append_tax(plan_iteration, year, rate, rmd)
            change = self._append_reinvestment(plan_iteration, income,
                                               tax, expense, rmd, year)
            total = self._append_accounts(plan_iteration, year,
                                          rate, change, plan_iteration != 0)
            self._append_percent_pulled(plan_iteration, change, total)

        return self.balances
