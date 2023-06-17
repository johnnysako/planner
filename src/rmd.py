class Rmd:
    def __init__(self, config):
        self.config = config

    def getRate(self, age):
        for entry in self.config:
            if entry.get("age") == age:
                return entry.get("rate")
        return 0