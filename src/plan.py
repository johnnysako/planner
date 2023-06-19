class Plan:
    def __init__(self, config):
        self.config = config

    def get_growth(self):
        return self.config.get("average_growth")
