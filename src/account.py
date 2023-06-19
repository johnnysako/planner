class Account:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config.get("name")

    def get_owner(self):
        return self.config.get("owner")

    def get_type(self):
        return self.config.get("type")

    def get_withdrawl_priority(self):
        return self.config.get("withdrawl_priority")

    def get_balance(self):
        return self.config.get("balance")

    def withdrawl(self, amount):
        new_balance = self.config.get("balance") - amount
        if new_balance >= 0:
            self.config.update({"balance": new_balance})
            return True
        else:
            return False
        
    def process_growth(self, rate):
        new_balance = self.config.get("balance") * (1 + rate/100) + self.config.get("annual_additions")
        self.config.update({"balance": new_balance})