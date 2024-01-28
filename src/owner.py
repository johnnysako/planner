class Owner:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["Name"]

    def get_age(self, year):
        return year - self.config["Year of Birth"]

    def get_retirement_age(self):
        return self.config["Retirement Age"]

    def get_social_security(self):
        return self.config["Social Security"]

    def get_life(self):
        return self.config["Life Expectancy"]

    def years_to_live(self, current_year):
        return self.config["Life Expectancy"] - self.get_age(current_year) + 1

    def is_retired(self, year):
        return year-self.config["Year of Birth"] > self.config["Retirement Age"]

    def retired_year(self):
        return self.config["Year of Birth"] + self.config["Retirement Age"]+1

    def get_income(self, include_social_security, year):
        if not self.is_retired(year):
            return self.config["Pre-retirement Take Home Pay"]
        elif include_social_security \
                and self.get_age(year) >= self.config["Age Starts Social Security"]:
            return self.get_social_security()
        return 0
