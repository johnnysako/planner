class Expense:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["name"]

    def is_need(self):
        return self.config["need"]
        
    def get_expense(self, year):
        if year < self.config["starting_year"]:
            return 0
        if (year - self.config["starting_year"]) % self.config["frequency"] == 0:
            return self.config["ammount"]
        return 0