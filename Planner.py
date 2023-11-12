import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow

# from src.account import Account
from src.owner import Owner
from src.expenses import Expenses
from src.expense import Expense
from src.account import Account


class JsonTableWindow(QWidget):
    def __init__(self, data, title):
        super().__init__()

        self.init_ui(data, title)

    def init_ui(self, data, title):
        self.owners = data
        # Create table widget
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(len(data[0].config))
        self.table_widget.setRowCount(len(data))

        # Set headers
        headers = list(data[0].config.keys())
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Populate the table
        for row_num, row_data in enumerate(data):
            for col_num, col_key in enumerate(headers):
                try:
                    item = QTableWidgetItem(str(row_data.config[col_key]))
                    self.table_widget.setItem(row_num, col_num, item)
                except KeyError:
                    print('Missing Key (could be optional)', file=sys.stderr)

        # Connect the itemChanged signal to a custom slot
        self.table_widget.itemChanged.connect(self.on_item_changed)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)

        # Set window properties
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)

    def on_item_changed(self, item):
        # Get the row and column of the changed item
        row = item.row()
        col = item.column()

        # Update the corresponding Owner object in the data
        self.owner = self.owners[row]
        self.owner.config[self.table_widget.horizontalHeaderItem(col)
                          .text()] = item.text()


class MainWindow(QMainWindow):
    def load_constants(self, path):
        try:
            with open(os.path.join(path, 'owners.json')) as f:
                owners_data = json.load(f).get("owners", [])
                self.owners = [Owner(owner_data) for owner_data in owners_data]
        except FileNotFoundError:
            print('File not found', file=sys.stderr)
        except json.JSONDecodeError:
            print('Error decoding Owner JSON file', file=sys.stderr)

        try:
            with open(os.path.join(path, 'expenses.json')) as f:
                expense_data = json.load(f).get("expenses", [])
                self.expenses_data = [Expense(expense)
                                      for expense in expense_data]
                self.expenses = Expenses(self.expenses_data)
        except FileNotFoundError:
            print('File not found', file=sys.stderr)
        except json.JSONDecodeError:
            print('Error decoding Expense JSON file', file=sys.stderr)

        try:
            with open(os.path.join(path, 'accounts.json')) as f:
                account_data = json.load(f).get("accounts", [])
                self.accounts = [Account(account_data)
                                 for account_data in account_data]
        except FileNotFoundError:
            print('File not found', file=sys.stderr)
        except json.JSONDecodeError:
            print('Error decoding Owner JSON file', file=sys.stderr)

    def __init__(self):
        super().__init__()

        self.load_constants('')
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label = QLabel('Enter Data Path')
        self.entry = QLineEdit()
        self.owner_button = QPushButton('View Owner Data', self)
        self.expense_button = QPushButton('View Expense Data', self)
        self.account_button = QPushButton('View Account Data', self)
        self.path_button = QPushButton('Update Path', self)

        # Connect button click event to a function
        self.path_button.clicked.connect(self.on_path_click)
        self.owner_button.clicked.connect(self.on_owner_click)
        self.expense_button.clicked.connect(self.on_expense_click)
        self.account_button.clicked.connect(self.on_account_click)

        # Set up the app
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.path_button)
        layout.addWidget(self.owner_button)
        layout.addWidget(self.expense_button)
        layout.addWidget(self.account_button)

        self.setCentralWidget(central_widget)

        # Set window properties
        self.setWindowTitle('Planner')
        self.setGeometry(100, 100, 400, 200)
        self.show()

    def on_path_click(self):
        path = self.entry.text()
        self.load_constants(path)
        self.label.setText(f'Data Loaded From:, {path}')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
