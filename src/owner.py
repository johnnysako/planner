class Owner:
    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config.get("name")

    def get_age(self):
        return self.config.get("age")

    def get_retirement_age(self):
        return self.config.get("retirement_age")

    def get_social_security(self):
        return self.config.get("social_security")

    def trial_social_security(self):
        return self.config.get("trial_social_security")
