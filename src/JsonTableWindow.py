import copy
import sys

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QWidget, QHBoxLayout


class JsonTableWindow(QWidget):
    def __init__(self, main_window, data, title):
        super().__init__()

        self.main_window = main_window
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

    def closeEvent(self, event):
        self.main_window.show()
        event.accept()  # Accept the close event
