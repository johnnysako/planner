class Expense:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["Description"]

    def get_expense(self, year):
        end_year = self.config.get("Year Ends", 9999)

        if year < self.config["Year Starts"] or year > end_year:
            return 0
        elif (year - self.config["Year Starts"]) \
                % self.config["Every x Year(s)"] == 0:
            return self.config["Cost"]
        return 0
