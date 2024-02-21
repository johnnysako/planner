from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedWidget
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
        self.create_stacked_widgets()
        self.create_combobox()
        self.create_expense_summary()
        self.create_layout()

        self.setWindowTitle('Explore Data')
        self.showMaximized()

    def create_buttons(self):
        self.save_pdf_button = QPushButton('Save Result PDF', self)
        self.save_pdf_button.clicked.connect(self.save_pdf)

        self.average_button = QCheckBox('Average Results', self)
        self.average_button.clicked.connect(self.average_clicked)
        self.average_button.setChecked(True)

        self.index_select = QSpinBox(self)
        self.index_select.setMaximum(999)
        self.index_select.setMinimum(0)
        self.index_select.setValue(0)
        self.index_select.valueChanged.connect(self.index_changed)
        self.index_select.setEnabled(False)

    def create_combobox(self):
        self.combo_box = QComboBox(self)
        self.combo_box.currentIndexChanged.connect(self.update_trial)
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

    def create_stacked_widgets(self):
        self.mc_plot_stacked_widget = QStackedWidget()
        self.gain_loss_chart = QStackedWidget()
        self.mc_summary_stacked_widget = QStackedWidget()
        self.average_tax = QStackedWidget()
        self.result_graph = QStackedWidget()
        self.expense = QStackedWidget()

        for trial_data in self.results['trials_data']:
            self.add_mc_plot_widget(trial_data)
            self.add_gain_loss_widget(trial_data)
            self.add_mc_summary_widget(trial_data)
            self.create_tax_summary(trial_data)

        self.add_single_plot()
        self.add_single_rates()
        self.add_single_tax()

    def add_mc_plot_widget(self, trial_data):
        monte_carlos_figure = Figure()
        self.monte_carlos_canvas = FigureCanvas(monte_carlos_figure)
        mc_plot_widget = QWidget()
        mc_plot_layout = QVBoxLayout()
        plot_monte_carlos(trial_data['sorted_data'],
                          trial_data['failed_plans'],
                          self.results['owners'],
                          trial_data['trial'],
                          self.monte_carlos_canvas)
        mc_plot_layout.addWidget(self.monte_carlos_canvas)
        mc_plot_widget.setLayout(mc_plot_layout)
        self.mc_plot_stacked_widget.addWidget(mc_plot_widget)

    def add_gain_loss_widget(self, trial_data):
        gain_loss_widget = QWidget()
        gain_loss_layout = QVBoxLayout()

        _, average_stock, average_bond, _ = process_average(
            trial_data['sorted_data'])
        canvas = FigureCanvas(Figure())
        plot_gains_losses(
            trial_data['sorted_data'][0]['Year'],
            average_stock, average_bond, canvas)
        gain_loss_layout.addWidget(canvas)
        gain_loss_widget.setLayout(gain_loss_layout)
        self.gain_loss_chart.addWidget(gain_loss_widget)

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
                      self.single_tax_canvas)

    def add_single_tax(self):
        single_tax_figure = Figure()
        self.single_tax_canvas = FigureCanvas(single_tax_figure)
        self.update_single_tax(0, 0)

    def update_single_plot(self, trial, index):
        plot_single(self.results['trials_data'][trial]['sorted_data'][index],
                    self.results['owners'],
                    self.results['trials_data'][trial]['trial'],
                    index, self.single_result_canvas)

    def add_single_plot(self):
        single_result_figure = Figure()
        self.single_result_canvas = FigureCanvas(single_result_figure)
        self.update_single_plot(0, 0)
        self.single_run = QWidget()
        single_run_layout = QVBoxLayout()
        single_run_layout.addWidget(self.single_result_canvas)
        self.single_run.setLayout(single_run_layout)

    def update_rates(self, trial, index):
        plot_gains_losses(
            self.results['trials_data'][trial]
            ['sorted_data'][index]['Year'],
            self.results['trials_data'][trial]
            ['sorted_data'][index]['Stock Returns'],
            self.results['trials_data'][trial]
            ['sorted_data'][index]['Bond Returns'],
            self.single_rate_canvas)

    def add_single_rates(self):
        single_rate = Figure()
        self.single_rate_canvas = FigureCanvas(single_rate)
        self.update_rates(0, 0)
        self.single_gain_loss_chart = QWidget()
        single_gain_loss_layout = QVBoxLayout()
        single_gain_loss_layout.addWidget(self.single_rate_canvas)
        self.single_gain_loss_chart.setLayout(single_gain_loss_layout)

    def add_mc_summary_widget(self, trial_data):
        mc_summary = Figure()
        self.mc_summary_canvas = FigureCanvas(mc_summary)
        summary, labels = summarize_data(trial_data['sorted_data'])
        draw_as_table(summary, "Monte Carlos Summary",
                      labels, self.mc_summary_canvas)
        self.mc_summary_stacked_widget.addWidget(self.mc_summary_canvas)

    def create_expense_summary(self):
        expense_summary = Figure()
        expense_summary_b = Figure()
        self.expense_summary = FigureCanvas(expense_summary)
        self.expense_summary_b = FigureCanvas(expense_summary_b)
        data = generate_expense_over_time(self.results['expenses'],
                                          self.results['start_year'],
                                          self.results['years_to_process'])
        plot_expenses_summary(data, self.expense_summary)
        plot_expenses_summary(data, self.expense_summary_b)

    def create_tax_summary(self, trial_data):
        mc_tax_summary = Figure()
        self.mc_tax_summary_canvas = FigureCanvas(mc_tax_summary)

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
        draw_as_table(summary, "Tax Breakdown Summary",
                      labels, self.mc_tax_summary_canvas)
        self.average_tax.addWidget(self.mc_tax_summary_canvas)

    def create_layout(self):
        graph_expense_rates = QVBoxLayout()
        graph_expense_rates.addWidget(self.mc_plot_stacked_widget, 4)
        graph_expense_rates.addWidget(self.gain_loss_chart, 1)

        single_graph_run = QVBoxLayout()
        single_graph_run.addWidget(self.single_run, 4)
        single_graph_run.addWidget(self.single_gain_loss_chart, 1)

        self.result_graph.addWidget(QWidget())
        self.result_graph.addWidget(QWidget())
        self.result_graph.widget(0).setLayout(graph_expense_rates)
        self.result_graph.widget(1).setLayout(single_graph_run)

        graph_expense_tax = QVBoxLayout()
        graph_expense_tax.addWidget(self.expense_summary, 4)
        graph_expense_tax.addWidget(self.average_tax, 2)

        single_expense_tax = QVBoxLayout()
        single_expense_tax.addWidget(self.expense_summary_b, 4)
        single_expense_tax.addWidget(self.single_tax_canvas, 2)

        self.expense.addWidget(QWidget())
        self.expense.addWidget(QWidget())
        self.expense.widget(0).setLayout(graph_expense_tax)
        self.expense.widget(1).setLayout(single_expense_tax)

        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.result_graph, 2)
        graph_layout.addWidget(self.expense, 2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.combo_box)
        button_layout.addWidget(self.average_button)
        button_layout.addWidget(self.index_select)
        button_layout.addWidget(self.save_pdf_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(graph_layout, 3)
        main_layout.addWidget(self.mc_summary_stacked_widget, 1)
        main_layout.addLayout(button_layout)

    def update_trial(self):
        index = self.combo_box.currentIndex()
        self.mc_summary_stacked_widget.setCurrentIndex(index)
        self.mc_plot_stacked_widget.setCurrentIndex(index)
        self.gain_loss_chart.setCurrentIndex(index)
        self.average_tax.setCurrentIndex(index)
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

    def average_clicked(self):
        self.index_select.setEnabled(not self.average_button.isChecked())
        self.result_graph.setCurrentIndex(
            int(not self.average_button.isChecked()))
        self.expense.setCurrentIndex(
            int(not self.average_button.isChecked()))
        self.index_changed()

    def index_changed(self):
        self.update_single_plot(self.combo_box.currentIndex(),
                                self.index_select.value())
        self.update_rates(self.combo_box.currentIndex(),
                          self.index_select.value())
        self.update_single_tax(self.combo_box.currentIndex(),
                               self.index_select.value())
