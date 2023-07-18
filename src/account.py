def rmd_applies(account_type):
    rmd_types = ["401K", "IRA"]
    for type in rmd_types:
        if type == account_type:
            return True
    return False

class Account:
    def __init__(self, config):
        valid_types = ["401K", "Roth", "IRA", "Investment", "HSA"]
        for type in valid_types:
            if type == config["type"]:
                self.config = config
                return
        raise TypeError

    def get_name(self):
        return self.config["name"]

    def get_owner(self):
        return self.config["owner"]

    def get_type(self):
        return self.config["type"]

    def is_taxable(self):
        return self.get_type() == "Investment"

    def get_withdrawl_priority(self):
        return self.config["withdrawl_priority"]

    def get_balance(self):
        return self.config["balance"]

    def withdrawl_rmd(self, rate):
        rmd = 0
        if rmd_applies(self.get_type()):
            rmd = self.config["balance"] * rate/100
        self.config["balance"] = round(self.config["balance"] - rmd, 2)
        return rmd 
        
    def withdrawl(self, amount):
        new_balance = self.config["balance"] - amount

        if new_balance >= 0:
            self.config["balance"] = round(new_balance, 2)
            return True
        else:
            return False
        
    def process_growth(self, rate, interest_only=False):
        if interest_only:
            new_balance = self.config["balance"] * (1 + rate/100)
        else:
            new_balance = self.config["balance"] * (1 + rate/100) + self.config["annual_additions"]
        self.config["balance"] = round(new_balance, 2)