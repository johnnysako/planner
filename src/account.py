def rmd_applies(account_type, roth_with_rmd):
    rmd_types = ["401K", "IRA"]
    for type in rmd_types:
        if type == account_type:
            return True
    if account_type == "Roth" and roth_with_rmd:
        return True
    return False


class Account:
    def __init__(self, config):
        if "allocation" in config:
            config["allocation"] = sorted(config["allocation"],
                                          key=lambda x: x["year"],
                                          reverse=True)

            for item in config["allocation"]:
                if item["bonds"] + item["stocks"] != 100:
                    raise TypeError

        valid_types = ["401K", "Roth", "IRA", "Investment", "HSA"]
        for type in valid_types:
            if type == config["type"]:
                self.config = config
                return

        raise TypeError

    def get_growth(self, year, rates):
        if "allocation" not in self.config:
            print(year, rates)
            return self.config["balance"] * rates["s"]/100

        growth_s = self.config["balance"] \
            * self.get_allocation(year, "stocks")/100 \
            * rates["s"]/100
        growth_b = self.config["balance"] \
            * self.get_allocation(year, "bonds")/100 \
            * rates["b"]/100
        return growth_s + growth_b

    def get_name(self):
        return self.config["name"]

    def get_owner(self):
        return self.config["owner"]

    def get_type(self):
        return self.config["type"]

    def is_taxable(self):
        return self.get_type() == "Investment"

    def get_balance(self):
        return self.config["balance"]

    def get_allocation(self, year, type):
        if "allocation" not in self.config:
            return 100 if type == "stocks" else 0
        for entry in self.config["allocation"]:
            if entry["year"] <= year:
                return entry[type]
        return 100 if type == "stocks" else 0

    def withdraw_rmd(self, rate, roth_with_rmd=False):
        rmd = 0
        if rmd_applies(self.get_type(),
                       self.config["trail_with_rmd"]
                       and roth_with_rmd) and rate != 0:
            rmd = self.config["balance"] / rate
        self.config["balance"] = round(self.config["balance"] - rmd, 2)
        return rmd

    def withdraw(self, amount):
        new_balance = self.config["balance"] - amount

        if new_balance >= 0:
            self.config["balance"] = round(new_balance, 2)
            return True
        else:
            return False

    def process_growth(self, year, rates, interest_only=False):
        growth = self.get_growth(year, rates)

        if interest_only:
            new_balance = self.config["balance"] + growth
        else:
            new_balance = self.config["balance"] \
                + growth + self.config["annual_additions"]
        self.config["balance"] = round(new_balance, 2)
