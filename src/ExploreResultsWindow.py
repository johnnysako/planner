from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedWidget
from PyQt5.QtWidgets import QComboBox

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

        self.mc_plot_stacked_widget = QStackedWidget()
        self.mc_summary_stacked_widget = QStackedWidget()

        self.combo_box = QComboBox(self)
        self.combo_box.currentIndexChanged.connect(self.update_trial)

        self.combo_box.addItem('Base Projection')

        for trial_data in self.results['trials_data']:
            if trial_data['trial']['rmd']:
                self.combo_box.addItem('With RMD on Select Accounts')

            if not trial_data['trial']['Social Security']:
                self.combo_box.addItem('Without Social Security')

            if trial_data['trial']['bad_timing']:
                self.combo_box.addItem("Bad Timing")

            self.mc_plot_stacked_widget.addWidget(
                plot_monte_carlos(trial_data['sorted_data'],
                                  trial_data['failed_plans'],
                                  self.results['owners'],
                                  trial_data['trial']))

            _, summary, labels = summarize_data(trial_data['sorted_data'])
            self.mc_summary_stacked_widget.addWidget(
                get_data_table_canvas(summary,
                                      "Monte Carlos Summary",
                                      labels))

        data = generate_expense_over_time(self.results['expenses'],
                                          self.results['start_year'],
                                          self.results['years_to_process'])
        self.expense_summary = plot_expenses_summary(data)

        # Set up layout
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.mc_plot_stacked_widget, 1)
        graph_layout.addWidget(self.expense_summary, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.combo_box)
        button_layout.addWidget(self.save_pdf_button)

        layout = QVBoxLayout(self)
        layout.addLayout(graph_layout, 2)
        layout.addWidget(self.mc_summary_stacked_widget, 1)
        layout.addLayout(button_layout)

        self.setWindowTitle('Explore Data')
        self.showMaximized()

    def update_trial(self):
        self.mc_summary_stacked_widget.setCurrentIndex(
            self.combo_box.currentIndex())
        self.mc_plot_stacked_widget.setCurrentIndex(
            self.combo_box.currentIndex())

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
