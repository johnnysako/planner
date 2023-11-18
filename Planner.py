import sys
import os
import json
import copy
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow

# from src.account import Account
from src.owner import Owner
from src.expenses import Expenses
from src.expense import Expense
from src.account import Account
import PyFinancialPlanner as plan


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
        self.add_button = QPushButton('Add Row', self)
        self.remove_button = QPushButton('Delete Row', self)

        self.add_button.clicked.connect(self.add_row)
        self.remove_button.clicked.connect(self.delete_row)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)

        content_width = sum(self.table_widget.columnWidth(col)
                            for col in range(self.table_widget.columnCount()))

        content_height = sum(self.table_widget.rowHeight(row)
                             for row in range(self.table_widget.rowCount()))

        # Set window properties
        self.setWindowTitle(title)
        self.resize(content_width+75, content_height+75)

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

        self.load_constants('_internal')
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label = QLabel('Enter Data Path')
        self.entry = QLineEdit('_internal')
        self.owner_button = QPushButton('View Owner Data', self)
        self.expense_button = QPushButton('View Expense Data', self)
        self.account_button = QPushButton('View Account Data', self)
        self.path_button = QPushButton('Update Path', self)
        self.save_button = QPushButton('Save User Data', self)
        self.run_plan_button = QPushButton('Run Projection', self)

        # Connect button click event to a function
        self.path_button.clicked.connect(self.on_path_click)
        self.owner_button.clicked.connect(self.on_owner_click)
        self.expense_button.clicked.connect(self.on_expense_click)
        self.account_button.clicked.connect(self.on_account_click)
        self.save_button.clicked.connect(self.save_data_to_file)
        self.run_plan_button.clicked.connect(self.run_plan)

        # Set up the app
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.path_button)
        layout.addWidget(self.owner_button)
        layout.addWidget(self.expense_button)
        layout.addWidget(self.account_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.run_plan_button)

        self.setCentralWidget(central_widget)

        # Set window properties
        self.setWindowTitle('Planner')
        self.adjustSize()
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

    def save_data_to_file(self):
        path = self.entry.text()
        os_path = os.path.dirname(os.path.join(path, 'owners.json'))
        os.makedirs(os_path, exist_ok=True)

        data_to_save = [owner.config for owner in self.owners]
        with open(os.path.join(path, 'owners.json'), 'w') as f:
            json.dump({"owners": data_to_save}, f, indent=2)

        data_to_save = [expense.config for expense in self.expenses_data]
        with open(os.path.join(path, 'expenses.json'), 'w') as f:
            json.dump({"expenses": data_to_save}, f, indent=2)

        data_to_save = [account.config for account in self.accounts]
        with open(os.path.join(path, 'accounts.json'), 'w') as f:
            json.dump({"accounts": data_to_save}, f, indent=2)

    def run_plan(self):
        self.save_data_to_file()
        plan.main(self.entry.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
