from src.account import Account

class Plan:
    def __init__(self, config, accounts):
        self.config = config
        self.accounts = accounts

    def get_growth(self):
        return self.config["average_growth"]

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
                
