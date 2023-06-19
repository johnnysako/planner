class Tax:
    def __init__(self, config):
        self.config = config

    def calculate(self, income):
        previous_cutoff = 0

        for bracket in self.config:
            if bracket["cutoff"] == None or income < bracket["cutoff"]:
                break
            previous_cutoff = bracket["cutoff"]

        return (income-previous_cutoff)*bracket["rate"]/100 + bracket["max_tax_previous"]
