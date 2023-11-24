from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton

from src.generate_pdf import plot_pdf
from src.plot_monte_carlos import plot_monte_carlos
from src.plot_monte_carlos import summarize_data
from src.draw_table import get_data_table_canvas
from src.expenses import generate_expense_over_time
from src.expenses import plot_expenses_summary


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

        self.mc_canvas = plot_monte_carlos(self.results['trials_data'][0]
                                           ['sorted_data'],
                                           self.results['trials_data'][0]
                                           ['failed_plans'],
                                           self.results['owners'],
                                           self.results['trials_data'][0]
                                           ['trial'])

        _, summary, labels = summarize_data(self.results['trials_data']
                                            [0]
                                            ['sorted_data'])
        self.mc_summary = get_data_table_canvas(summary,
                                                "Monte Carlos Summary",
                                                labels)

        data = generate_expense_over_time(self.results['expenses'],
                                          self.results['start_year'],
                                          self.results['years_to_process'])
        self.expense_summary = plot_expenses_summary(data)

        # Set up layout
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.mc_canvas)
        graph_layout.addWidget(self.expense_summary)

        layout = QVBoxLayout(self)
        layout.addLayout(graph_layout)
        layout.addWidget(self.mc_summary)
        layout.addWidget(self.save_pdf_button)

        self.setWindowTitle('Explore Data')

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
