import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow

# from src.account import Account
from src.owner import Owner


class JsonOwnersWindow(QWidget):
    def __init__(self, owner_data):
        super().__init__()

        self.init_ui(owner_data)

    def init_ui(self, owner_data):
        # Create table widget
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(len(owner_data[0].config))
        table_widget.setRowCount(len(owner_data))

        # Set headers
        headers = list(owner_data[0].config.keys())
        table_widget.setHorizontalHeaderLabels(headers)

        # Populate the table
        for row_num, row_data in enumerate(owner_data):
            for col_num, col_key in enumerate(headers):
                item = QTableWidgetItem(str(row_data.config[col_key]))
                table_widget.setItem(row_num, col_num, item)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(table_widget)

        # Set window properties
        self.setWindowTitle('Owner Data')
        self.setGeometry(100, 100, 800, 600)


class MainWindow(QMainWindow):
    def load_constants(self, path):
        try:
            with open(os.path.join(path, 'owners.json')) as f:
                owners_data = json.load(f).get("owners", [])
                owners = [Owner(owner_data) for owner_data in owners_data]
                return owners
        except FileNotFoundError:
            print('File not found')
        except json.JSONDecodeError:
            print('Error decoding JSON file')

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label = QLabel('Enter Data Path')
        self.entry = QLineEdit()
        self.button = QPushButton('View Owner Data', self)

        # Connect button click event to a function
        self.button.clicked.connect(self.on_button_click)

        # Set up the app
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.button)

        self.setCentralWidget(central_widget)

        # Set window properties
        self.setWindowTitle('Planner')
        self.setGeometry(100, 100, 400, 200)
        self.show()

    def on_button_click(self):
        # Handle button click event
        path = self.entry.text()
        if len(path) != 0:
            path = path + '/'
        owners = self.load_constants(path)
        self.label.setText(f'Data Loaded From:, {path}')

        # Create and show the JSON table window
        self.owner_window = JsonOwnersWindow(owners)
        self.owner_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
