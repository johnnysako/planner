import sys
import os
import json
import copy
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox

# from src.account import Account
from src.owner import Owner
from src.expenses import Expenses
from src.expense import Expense
from src.account import Account
import PyFinancialPlanner as plan

import matplotlib
matplotlib.use('Qt5Agg')

basedir = os.path.dirname(__file__)


def convert_numeric_strings_to_numbers(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_numeric_strings_to_numbers(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_numeric_strings_to_numbers(item)
    elif isinstance(data, str):
        if data.isdigit():
            return int(data)
        elif data.replace(".", "").isdigit():
            return float(data)
    return data


class JsonTableWindow(QWidget):
    def __init__(self, data, title):
        super().__init__()

        self.init_ui(data, title)

    def init_ui(self, data, title):
        self.data = data
        self.headers = list(data[0].config.keys())

        # Create table widget
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(len(data[0].config))
        self.table_widget.setRowCount(len(data))

        # Set headers
        self.table_widget.setHorizontalHeaderLabels(self.headers)

        # Populate the table
        for row_num, row_data in enumerate(data):
            for col_num, col_key in enumerate(self.headers):
                try:
                    item = QTableWidgetItem(str(row_data.config[col_key]))
                    self.table_widget.setItem(row_num, col_num, item)
                except KeyError:
                    print('Missing Key (could be optional)', file=sys.stderr)

        self.table_widget.itemChanged.connect(self.on_item_changed)
        self.table_widget.resizeColumnsToContents()

        # Add buttons for add/delete rows
        add_button = QPushButton('Add Row', self)
        remove_button = QPushButton('Delete Row', self)

        add_button.clicked.connect(self.add_row)
        remove_button.clicked.connect(self.delete_row)

        # Set up button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)

        # Set window properties
        self.setWindowTitle(title)
        self.resize(1000, 500)

    def add_row(self):
        # Add a new row with default data
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        new_data_item = copy.deepcopy(self.data[-1])
        self.data.append(new_data_item)

        for col_num, col_key in enumerate(self.headers):
            try:
                item = QTableWidgetItem(str(self.data[-1].config[col_key]))
                self.table_widget.setItem(row_position, col_num, item)
            except KeyError:
                print('Missing Key (could be optional)', file=sys.stderr)

    def delete_row(self):
        # Delete the selected row
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.table_widget.removeRow(selected_row)
            del self.data[selected_row]

    def on_item_changed(self, item):
        # Get the row and column of the changed item
        row = item.row()
        col = item.column()

        # Update the corresponding value in the data model
        header = self.headers[col]
        self.data[row].config[header] = item.text()


class MainWindow(QMainWindow):
    def load_json(self, path, file_name, field):
        try:
            f = open(os.path.join(path, file_name))
        except FileNotFoundError:
            print('File not found, loading default example', file=sys.stderr)
            f = open(os.path.join(basedir, '_internal', file_name))

        try:
            return json.load(f).get(field, [])

        except json.JSONDecodeError:
            print('Error decoding Owner JSON file', file=sys.stderr)
            f = open(os.path.join(basedir, '_internal', file_name))
            return json.load(f).get(field, [])

    def load_constants(self):
        owners_data = self.load_json(self.path, 'owners.json', "owners")
        self.owners = [Owner(owner_data) for owner_data in owners_data]

        expense_data = self.load_json(self.path, 'expenses.json', "expenses")
        self.expenses_data = [Expense(expense) for expense in expense_data]
        self.expenses = Expenses(self.expenses_data)

        account_data = self.load_json(self.path, 'accounts.json', "accounts")
        self.accounts = [Account(account_data)
                         for account_data in account_data]

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.owner_button = QPushButton('View Owner Data', self)
        self.expense_button = QPushButton('View Expense Data', self)
        self.account_button = QPushButton('View Account Data', self)
        self.load_data = QPushButton('Load User Data', self)
        self.save_button = QPushButton('Save User Data', self)
        self.run_plan_button = QPushButton('Run Projection', self)
        self.inc_social_security = \
            QCheckBox('Test Without Social Security', self)
        self.test_rmd = QCheckBox('Test With RMD on Select Accounts', self)

        # Connect button click event to a function
        self.load_data.clicked.connect(self.on_load_data)
        self.owner_button.clicked.connect(self.on_owner_click)
        self.expense_button.clicked.connect(self.on_expense_click)
        self.account_button.clicked.connect(self.on_account_click)
        self.save_button.clicked.connect(self.save_data_to_file)
        self.run_plan_button.clicked.connect(self.run_plan)

        # Disable buttons until data is loaded
        self.owner_button.setEnabled(False)
        self.expense_button.setEnabled(False)
        self.account_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.run_plan_button.setEnabled(False)

        # Set up the app
        central_widget = QWidget(self)

        save_load_layout = QHBoxLayout()
        save_load_layout.addWidget(self.load_data)
        save_load_layout.addWidget(self.save_button)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.owner_button)
        data_layout.addWidget(self.expense_button)
        data_layout.addWidget(self.account_button)

        layout = QVBoxLayout(central_widget)
        layout.addLayout(data_layout)
        layout.addWidget(self.inc_social_security)
        layout.addWidget(self.test_rmd)
        layout.addWidget(self.run_plan_button)
        layout.addLayout(save_load_layout)

        self.setCentralWidget(central_widget)

        # Set window properties
        self.setWindowTitle('Planner')
        self.adjustSize()
        self.show()

    def on_load_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog

        self.path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                     options=options)
        self.load_constants()
        self.save_data_to_file()

        # Enable buttons since data is loaded
        self.owner_button.setEnabled(True)
        self.expense_button.setEnabled(True)
        self.account_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.run_plan_button.setEnabled(True)

    def on_owner_click(self):
        self.owner_window = JsonTableWindow(self.owners, "Owner Data")
        self.owner_window.show()

    def on_expense_click(self):
        self.expense_window = JsonTableWindow(self.expenses_data,
                                              "Expense Data")
        self.expense_window.show()

    def on_account_click(self):
        self.account_window = JsonTableWindow(self.accounts,
                                              "Account Data")
        self.account_window.show()

    def save_data_to_file(self):
        data_to_save = [owner.config for owner in self.owners]
        converted_data = convert_numeric_strings_to_numbers(data_to_save)
        with open(os.path.join(self.path, 'owners.json'), 'w') as f:
            json.dump({"owners": converted_data}, f, indent=2)

        data_to_save = [expense.config for expense in self.expenses_data]
        converted_data = convert_numeric_strings_to_numbers(data_to_save)
        with open(os.path.join(self.path, 'expenses.json'), 'w') as f:
            json.dump({"expenses": converted_data}, f, indent=2)

        data_to_save = [account.config for account in self.accounts]
        converted_data = convert_numeric_strings_to_numbers(data_to_save)
        with open(os.path.join(self.path, 'accounts.json'), 'w') as f:
            json.dump({"accounts": converted_data}, f, indent=2)

    def run_plan(self):
        self.save_data_to_file()
        plan.main(personal_path=self.path,
                  with_social=self.inc_social_security.isChecked(),
                  with_rmd_trial=self.test_rmd.isChecked(),
                  display_charts=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
