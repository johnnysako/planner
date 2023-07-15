from src.account import Account
from src.owner import Owner

def owner_is_not_known(name, owners):
    for owner in owners:
        if owner.get_name() == name: return False
    return True

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
        header_string = ""
        for account in self.accounts:
            header_string += account.get_name() + ","
        
        header_string = header_string.rstrip(',')
        return header_string

    def process_growth(self, years):
        balances = []

        for i in range(years+1):
            balances.append([])
            for account in self.accounts:
                if i>=1:
                    account.process_growth(self.config["average_growth"])
                balances[i].append(account.get_balance())
        return balances
                
