from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QComboBox, QCheckBox, QSpinBox

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas

from src.generate_pdf import plot_pdf
from src.plot_monte_carlos import plot_monte_carlos
from src.plot_monte_carlos import summarize_data
from src.plot_monte_carlos import process_average
from src.plot_monte_carlos import plot_gains_losses
from src.plot_monte_carlos import plot_single
from src.plot_monte_carlos import average_tax_data
from src.plot_monte_carlos import summarize_tax_data
from src.draw_table import draw_as_table
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
        self.create_buttons()
        self.draw_initial_canvas()
        self.create_combobox()
        self.create_expense_summary()
        self.create_layout()

        self.setWindowTitle('Explore Data')
        self.showMaximized()

    def create_buttons(self):
        self.save_pdf_button = QPushButton('Save Result PDF', self)
        self.save_pdf_button.clicked.connect(self.save_pdf)

        self.average_button = QCheckBox('Average Results', self)
        self.average_button.clicked.connect(self.index_changed)
        self.average_button.setChecked(True)

        self.index_select = QSpinBox(self)
        self.index_select.setMaximum(999)
        self.index_select.setMinimum(0)
        self.index_select.setValue(0)
        self.index_select.valueChanged.connect(self.index_changed)
        self.index_select.setEnabled(False)

    def create_combobox(self):
        self.combo_box = QComboBox(self)
        self.combo_box.currentIndexChanged.connect(self.index_changed)
        self.combo_box.addItem('Base Projection')

        for trial_data in self.results['trials_data']:
            trial_desc = ''
            if trial_data['trial']['rmd']:
                trial_desc = 'With RMD on Select Accounts'
            if not trial_data['trial']['Social Security']:
                trial_desc = 'Without Social Security'
            if trial_data['trial']['bad_timing']:
                trial_desc = 'Bad Timing'
            if trial_desc:
                self.combo_box.addItem(trial_desc)

    def draw_initial_canvas(self):
        self.monte_carlos_canvas = FigureCanvas(Figure())
        self.update_mc_plot_canvas(self.results['trials_data'][0])

        self.gain_loss_canvas = FigureCanvas(Figure())
        self.update_gain_loss_canvas(self.results['trials_data'][0])

        self.mc_summary_canvas = FigureCanvas(Figure())
        self.update_mc_summary(self.results['trials_data'][0])

        self.tax_canvas = FigureCanvas(Figure())
        self.update_tax_canvas(self.results['trials_data'][0])

    def update_mc_plot_canvas(self, trial_data):
        plot_monte_carlos(trial_data['sorted_data'],
                          trial_data['failed_plans'],
                          self.results['owners'],
                          trial_data['trial'],
                          self.monte_carlos_canvas)

    def update_single_plot(self, trial, index):
        plot_single(self.results['trials_data'][trial]['sorted_data'][index],
                    self.results['owners'],
                    self.results['trials_data'][trial]['trial'],
                    index, self.monte_carlos_canvas)

    def update_gain_loss_canvas(self, trial_data):
        _, average_stock, average_bond, _ = process_average(
            trial_data['sorted_data'])
        plot_gains_losses(
            trial_data['sorted_data'][0]['Year'],
            average_stock, average_bond, self.gain_loss_canvas)

    def update_single_gain_loss_canvas(self, trial, index):
        plot_gains_losses(
            self.results['trials_data'][trial]
            ['sorted_data'][index]['Year'],
            self.results['trials_data'][trial]
            ['sorted_data'][index]['Stock Returns'],
            self.results['trials_data'][trial]
            ['sorted_data'][index]['Bond Returns'],
            self.gain_loss_canvas)

    def update_tax_canvas(self, trial_data):
        summary = average_tax_data(trial_data['sorted_data'],
                                   self.results['owners'],
                                   self.results['account_base'])

        labels = summary['Year'].values.astype(int)
        summary.drop('Year', axis=1, inplace=True)
        summary.update(summary[['Taxable',
                                'Tax Deferred',
                                'Tax Sheltered',
                                'Total']].astype(float))
        summary.update(summary[['Taxable',
                                'Tax Deferred',
                                'Tax Sheltered',
                                'Total']].applymap('${:,.0f}'.format))
        draw_as_table(summary, "Tax Breakdown Summary", labels,
                      self.tax_canvas)

    def update_single_tax(self, trial, index):
        summary = summarize_tax_data(self.results['trials_data'][trial]
                                     ['sorted_data'][index],
                                     self.results['owners'],
                                     self.results['account_base'])

        labels = summary['Year'].values.astype(int)
        summary.drop('Year', axis=1, inplace=True)
        summary.update(summary[['Taxable', 'Tax Deferred', 'Tax Sheltered',
                                'Total']].astype(float))
        summary.update(summary[['Taxable', 'Tax Deferred', 'Tax Sheltered',
                                'Total']].applymap('${:,.0f}'.format))

        draw_as_table(summary, "Tax Breakdown Summary", labels,
                      self.tax_canvas)

    def update_mc_summary(self, trial_data):
        summary, labels = summarize_data(trial_data['sorted_data'])
        draw_as_table(summary, "Monte Carlos Summary",
                      labels, self.mc_summary_canvas)

    def create_expense_summary(self):
        self.expense_summary = FigureCanvas(Figure())
        data = generate_expense_over_time(self.results['expenses'],
                                          self.results['start_year'],
                                          self.results['years_to_process'])
        plot_expenses_summary(data, self.expense_summary)

    def create_layout(self):
        graph_expense_rates = QVBoxLayout()
        graph_expense_rates.addWidget(self.monte_carlos_canvas, 4)
        graph_expense_rates.addWidget(self.gain_loss_canvas, 1)

        graph_expense_tax = QVBoxLayout()
        graph_expense_tax.addWidget(self.expense_summary, 4)
        graph_expense_tax.addWidget(self.tax_canvas, 2)

        graph_layout = QHBoxLayout()
        graph_layout.addLayout(graph_expense_rates, 2)
        graph_layout.addLayout(graph_expense_tax, 2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.combo_box)
        button_layout.addWidget(self.average_button)
        button_layout.addWidget(self.index_select)
        button_layout.addWidget(self.save_pdf_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(graph_layout, 3)
        main_layout.addWidget(self.mc_summary_canvas, 1)
        main_layout.addLayout(button_layout)

        self.index_changed()
        self.index_changed()

    def save_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
        path = QFileDialog.getExistingDirectory(self, "Select Folder to Save",
                                                options=options)
        if path:
            plot_pdf(self.results['trials_data'], self.results['owners'],
                     self.results['expenses'], self.results['start_year'],
                     self.results['years_to_process'], self.path, path)

    def closeEvent(self, event):
        self.main_window.show()
        event.accept()

    def index_changed(self):
        trial_selected = self.combo_box.currentIndex()
        trial_index = self.index_select.value()
        average = self.average_button.isChecked()

        self.index_select.setEnabled(not average)

        if average:
            trial_data = self.results['trials_data'][trial_selected]
            self.update_mc_plot_canvas(trial_data)
            self.update_gain_loss_canvas(trial_data)
            self.update_tax_canvas(trial_data)
            self.update_mc_summary(trial_data)

        else:
            self.update_single_plot(trial_selected, trial_index)
            self.update_single_gain_loss_canvas(trial_selected, trial_index)
            self.update_single_tax(trial_selected, trial_index)
