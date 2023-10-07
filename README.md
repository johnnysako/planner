## Retirement Projection
![](images/example_result.jpg)
This tool was built to be able to run comparisons of a few different scenarios for retirement. First and foremost it was built to understand the impact on a plan of using a Roth 401K vs a Traditional 401K. Most financial projections make this comparison difficult at best. Second, the plan will run with and without social security.

This has been built to be very configurable (probably too configurable) on expenses and timing of those expenses and will generate a graph and table of the expenses over the course of the plan.
![](images/example_expense.jpg)

This does run a Monte Carlos simulation of 4 different scenarios:
- With Social Security, Selected Roth do NOT have RMDs
- With Social Security, Selected Roths DO have RMDs
- Without Social Security, Selected Roth do NOT have RMDs
- Without Social Security, Selected Roths DO have RMDs

This simulation does NOT adjust or account for inflation, so all numbers are in the dollar amount for the simulation start year (set to 2023 in `PyFinancialPlanner.py`). This will generate a random number for each year of the financial plan as the growth for that year.

Some notes: When it comes time to withdrawl funds to cover expenses (i.e. income from sources such as RMD, income, social security) the program will pull funds from the first account it finds in `accounts.json` until it reaches 0 and then move to the next account. Once an account is at 0 it is effectively "closed".

## Configuration
There are several files needed for configuration of this tool:
- `accounts.json`
- `expenses.json`
- `owners.json`

This program also has two files included as "adjustable" in the event that the government changes something tax wise:
- `rmd.json`
- `tax.json`

### `accounts.json`
```
{
    "accounts": [
        {
            "name": "Account Name A", 
            "balance": 123456.78,
            "annual_additions": 0.0, 
            "type": "Investment",
            "owner": "Owner 1",
            "trail_with_rmd": false
        },
        {
            "name": "Account Name B",
            "balance": 876543.21,
            "annual_additions": 0.0,
            "type": "401K",
            "owner": "Owner 2",
            "trail_with_rmd": false
        }
    ]
}
```
- `"name"`: This is just a lable, name it whatever you want. Nothing was tested with two accounts having the same name...
- `"balance"`: Self describing
- `"annual_additions"`: If the account has funds added (like 401K while working), add that here
- `"type"`: Options:
  - `"401K"` or `"IRA"`: Has RMDs, distributions taxed
  - `"Roth"`: Does not have RMD (unless trialed with), not taxed
  - `"Investment"`: Growth taxed annually
  - `"HSA"`: Not taxed, no RMD
- `"owner"`: Must be in the list of `owners.json`
- `"trial_with_rmd"`: If the account type is `"Roth"` the program will run a simulation in which this account will have RMDs

### `expenses.json`
```
{
    "expenses": [
        {
            "name": "Living",
            "need": true,
            "ammount": 60000,
            "starting_year": 2023,
            "end_year": 2042,
            "frequency": 1
        },
        {
            "name": "Living Jack Joe Retired",
            "need": true,
            "ammount": 50000,
            "starting_year": 2043,
            "end_year": 2049,
            "frequency": 1
        }
    ]
}
```
- `"name"`: Just a label
- `"need"`: Not used yet, this is for future use in simulating plan success with wants vs needs
- `"ammount"`: How much is the expense annually?
- `"starting_year"`: Year the expense starts
- `"end_year"`: Year the expense ends [optional] - if not included expense will run to end of plan
- `"frequency"`: How many years between expenses? For example, 5 means the expense happens every 5th year (2043, 2048, 2053, etc.)
### `owners.json`
```
{
    "owners": [
        {
            "name": "Jane Doe",
            "birth_year": 1980,
            "life": 99,
            "retirement_age": 70,
            "income": 90000,
            "social_security": 20000,
            "start_social_security": 70,
            "trial_social_security": true
        },
        {
            "name": "Jack Joe",
            "birth_year": 1975,
            "life": 99,
            "retirement_age": 68,
            "income": 50000,
            "social_security": 15000,
            "start_social_security": 70,
            "trial_social_security": true
        }
    ]
}
```
- `"name"`: Just a lable
- `"birth_year"`: What year was this person born?
- `"life"`: How many years will this person live?
- `"retirement_age"`: What year will this person retire?
- `"income"`: What is the income while working?
- `"social_security"`: What social security is expected?
- `"start_social_security"`: What year will this person start to pull social security?
- `"trial_social_security"`: Future use.

## Usage
This has been developed with unit tests for some aspects. From the root directory run `pytest` and the unit tests will run:
```
===================================================================================== test session starts ======================================================================================
platform darwin -- Python 3.9.6, pytest-7.3.2, pluggy-1.0.0
rootdir: /Users/johnny_sako/dev/planner
plugins: anyio-3.6.2
collected 75 items                                                                                                                                                                             

test/account_test.py .......................                                                                                                                                             [ 30%]
test/expense_test.py .....                                                                                                                                                               [ 37%]
test/expenses_test.py .....                                                                                                                                                              [ 44%]
test/owner_test.py ...........                                                                                                                                                           [ 58%]
test/plan_test.py ....................                                                                                                                                                   [ 85%]
test/rmd_test.py .....                                                                                                                                                                   [ 92%]
test/tax_test.py ......                      
```

To run the plan simply execute:
```
python3 PyFinancialPlanner.py
```
It is possible to pu ta copy of `accounts.json`, `expenses.json`, and `owners.json` in a different folder and specify that when running:
```
python3 PyFinancialPlanner.py path_to_your_data
```
The results will be stored in a pdf file named financial_analysis.pdf

It is possible to see expanded details of the failed trials. This significantly adds to the time to run the program as pyplot does not appear to be terribly fast. In `plot_monte_carlos.py` uncomment the following:
```
    # _plot_failed_plans(failed_plans, pdf)
```