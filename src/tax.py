class Tax:
    def __init__(self, config):
        self.config = config

    def calculate(self, income):
        previous_cutoff = 0

        for bracket in self.config:
            if bracket.get("cutoff") == None or income < bracket.get("cutoff"):
                break
            previous_cutoff = bracket.get("cutoff")

        return (income-previous_cutoff)*bracket.get("rate")/100 + bracket.get("max_tax_previous")
