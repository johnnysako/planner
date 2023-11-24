# from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog
from PyQt5.QtWidgets import QWidget, QPushButton

from src.generate_pdf import plot_pdf


class ExploreResults(QWidget):
    def __init__(self, results, path):
        super().__init__()

        self.results = results
        self.path = path
        self.init_ui()

    def init_ui(self):
        self.save_pdf_button = QPushButton('Save Result PDF', self)

        self.save_pdf_button.clicked.connect(self.save_pdf)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.save_pdf_button)

        self.setWindowTitle('Explore Data')
        self.resize(1000, 500)

    def save_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog

        path = QFileDialog.getExistingDirectory(self, "Select Folder "
                                                     "to Save",
                                                     options=options)

        plot_pdf(self.results['trials_data'], self.results['owners'],
                 self.results['expenses'], self.results['start_year'],
                 self.results['years_to_process'], path)
