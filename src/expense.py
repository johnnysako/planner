class Expense:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["Description"]

    def is_need(self):
        return self.config["need"]

    def get_expense(self, year):
        try:
            end_year = self.config["Year Ends"]
        except KeyError:
            end_year = 9999

        if year < self.config["Year Starts"] or year > end_year:
            return 0
        elif (year - self.config["Year Starts"]) \
                % self.config["Every x Year(s)"] == 0:
            return self.config["Cost"]
        return 0
