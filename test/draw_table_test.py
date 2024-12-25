import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import matplotlib.pyplot as plt
from src.draw_table import draw_as_table, plot_data_table


def setup_mock_table(mock_table, num_rows, num_columns, row_color, col_color,
                     cell_colors):
    mock_table.get_celld = MagicMock(return_value={})
    for row in range(num_rows):
        for col in range(num_columns):
            cell_mock = MagicMock()
            if row == 0:
                cell_mock.get_facecolor.return_value = col_color
            elif col == -1:
                cell_mock.get_facecolor.return_value = row_color
            else:
                cell_mock.get_facecolor.return_value = cell_colors[row-1][col]
            mock_table.get_celld.return_value[(row, col)] = cell_mock
            mock_table.get_celld.return_value[(row, -1)] = MagicMock(
                get_facecolor=MagicMock(return_value=row_color))


def test_draw_as_table():
    df = pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': [4, 5, 6],
    })
    title = "Sample Title"
    rowlabels = ['Row1', 'Row2', 'Row3']

    # Mock the canvas
    canvas = MagicMock()
    canvas.figure = plt.figure()

    draw_as_table(df, title, rowlabels, canvas)

    ax = canvas.figure.gca()
    assert ax.get_title() == title
    assert canvas.draw.called

    the_table = ax.tables[0]
    num_rows, num_columns = len(df) + 1, len(df.columns)

    setup_mock_table(the_table, num_rows, num_columns,
                     'lightblue', 'lightblue', [
                         ['white', 'white'],
                         ['lightgray', 'lightgray'],
                         ['white', 'white'],
                     ])

    for row in range(1, num_rows):
        assert the_table.get_celld()[(row, -1)].get_facecolor() == 'lightblue'

    for col in range(num_columns):
        assert the_table.get_celld()[(0, col)].get_facecolor() == 'lightblue'

    alternating_colors = [
        ['white'] * len(df.columns), ['lightgray'] * len(df.columns)
    ] * len(df)
    alternating_colors = alternating_colors[:len(df)]

    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            expected_color = alternating_colors[i-1][j]
            assert the_table.get_celld()[(i, j)].get_facecolor() == \
                expected_color


@patch('src.draw_table.FigureCanvasQTAgg', spec=True)
def test_plot_data_table(mock_figure_canvas):
    data = pd.DataFrame({
        'Column1': [1, 2, 3, 4, 5, 6],
        'Column2': [7, 8, 9, 10, 11, 12],
    })
    rowlabels = ['Row1', 'Row2', 'Row3', 'Row4', 'Row5', 'Row6']
    title = "Sample Title"
    pdf = MagicMock()

    mock_canvas_instance = MagicMock()
    mock_figure_canvas.return_value = mock_canvas_instance

    plot_data_table(data, pdf, rowlabels, title, numpages=(2, 1),
                    pagesize=(11, 8.5))

    assert mock_figure_canvas.called
    assert pdf.savefig.called
    assert mock_canvas_instance.draw.called

    assert mock_canvas_instance.figure.clear.call_count == 2

    ax = mock_canvas_instance.figure.gca()
    the_table = ax.tables[0]
    num_rows, num_columns = len(data) // 2 + 1, len(data.columns)

    setup_mock_table(the_table, num_rows, num_columns,
                     'lightblue', 'lightblue', [
                         ['white', 'white'],
                         ['lightgray', 'lightgray'],
                         ['white', 'white'],
                     ])

    for row in range(1, num_rows):
        assert the_table.get_celld()[(row, -1)].get_facecolor() == 'lightblue'

    for col in range(num_columns):
        assert the_table.get_celld()[(0, col)].get_facecolor() == 'lightblue'

    alternating_colors = [
        ['white'] * len(data.columns), ['lightgray'] * len(data.columns)
    ] * len(data)
    alternating_colors = alternating_colors[:len(data)]

    for i in range(1, len(data) // 2 + 1):
        for j in range(len(data.columns)):
            expected_color = alternating_colors[i-1][j]
            assert the_table.get_celld()[(i, j)].get_facecolor() == \
                expected_color


if __name__ == "__main__":
    pytest.main()
