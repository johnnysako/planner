class Owner:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config["name"]

    def get_age(self):
        return self.config["age"]

    def get_retirement_age(self):
        return self.config["retirement_age"]

    def get_social_security(self):
        return self.config["social_security"]

    def trial_social_security(self):
        return self.config["trial_social_security"]
