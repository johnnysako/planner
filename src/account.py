class Account:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["name"]

    def get_owner(self):
        return self.config["owner"]

    def get_type(self):
        return self.config["type"]

    def get_withdrawl_priority(self):
        return self.config["withdrawl_priority"]

    def get_balance(self):
        return self.config["balance"]

    def withdrawl(self, amount):
        new_balance = self.config["balance"] - amount
        if new_balance >= 0:
            self.config.update({"balance": new_balance})
            return True
        else:
            return False
        
    def process_growth(self, rate):
        new_balance = self.config["balance"] * (1 + rate/100) + self.config["annual_additions"]
        self.config["balance"] = new_balance