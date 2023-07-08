class Owner:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["name"]

    def get_age(self, year):
        return year - self.config["birth_year"]

    def get_retirement_age(self):
        return self.config["retirement_age"]

    def get_social_security(self):
        return self.config["social_security"]

    def trial_social_security(self):
        return self.config["trial_social_security"]

    def get_income(self, include_social_security, year):
        if self.get_age(year) < self.get_retirement_age():
            return self.config["income"]
        elif include_social_security and self.get_age(year) >= self.config["start_social_security"]:
            return self.get_social_security()
        return 0