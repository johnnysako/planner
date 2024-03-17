class Tax:
    def __init__(self, config):
        self.config = config

    def calculate(self, income, filing_status):
        tax_profile = self.config.get(filing_status)
        if tax_profile is None:
            raise ValueError("Invalid filing status")

        previous_cutoff = 0
        for bracket in tax_profile:
            if bracket["cutoff"] is None or income < bracket["cutoff"]:
                break
            previous_cutoff = bracket["cutoff"]

        return (income - previous_cutoff) * bracket["rate"] / 100 \
            + bracket["max_tax_previous"]
