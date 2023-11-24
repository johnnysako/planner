# from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog
from PyQt5.QtWidgets import QWidget, QPushButton

from src.generate_pdf import plot_pdf
from src.plot_monte_carlos import plot_monte_carlos


class ExploreResults(QWidget):
    def __init__(self, main_window, results, path):
        super().__init__()

        self.results = results
        self.path = path
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.save_pdf_button = QPushButton('Save Result PDF', self)

        self.save_pdf_button.clicked.connect(self.save_pdf)
        self.canvas = plot_monte_carlos(self.results['trials_data'][0]
                                        ['sorted_data'],
                                        self.results['trials_data'][0]
                                        ['failed_plans'],
                                        self.results['owners'],
                                        self.results['trials_data'][0]
                                        ['trial'])

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
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
                 self.results['years_to_process'], self.path, path)

    def closeEvent(self, event):
        self.main_window.show()
        event.accept()  # Accept the close event
