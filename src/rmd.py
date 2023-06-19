class Rmd:
    def __init__(self, config):
        self.config = config

    def getRate(self, age):
        for entry in self.config:
            if entry["age"] == age:
                return entry["rate"]
        return 0