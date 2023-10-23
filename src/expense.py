class Expense:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["name"]

    def is_need(self):
        return self.config["need"]

    def get_expense(self, year):
        try:
            end_year = self.config["end_year"]
        except KeyError:
            end_year = 9999

        if year < self.config["starting_year"] or year > end_year:
            return 0
        elif (year - self.config["starting_year"]) \
                % self.config["frequency"] == 0:
            return self.config["ammount"]
        return 0
