import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import matplotlib.pyplot as plt
from src.draw_table import draw_as_table, plot_data_table


def setup_mock_table(mock_table, nrows, ncols, row_color, col_color,
                     cell_colors):
    mock_table.get_celld = MagicMock(return_value={})
    for row in range(nrows):
        for col in range(ncols):
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
    nrows, ncols = len(df) + 1, len(df.columns)

    setup_mock_table(the_table, nrows, ncols, 'lightblue', 'lightblue', [
        ['white', 'white'],
        ['lightgray', 'lightgray'],
        ['white', 'white'],
    ])

    for row in range(1, nrows):
        assert the_table.get_celld()[(row, -1)].get_facecolor() == 'lightblue'

    for col in range(ncols):
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
    # Create a sample dataframe
    data = pd.DataFrame({
        'Column1': [1, 2, 3, 4, 5, 6],
        'Column2': [7, 8, 9, 10, 11, 12],
    })
    rowlabels = ['Row1', 'Row2', 'Row3', 'Row4', 'Row5', 'Row6']
    title = "Sample Title"
    pdf = MagicMock()
    
    # Create a mock for the canvas
    mock_canvas_instance = MagicMock()
    mock_figure_canvas.return_value = mock_canvas_instance
    
    # Call the function
    plot_data_table(data, pdf, rowlabels, title, numpages=(2, 1),
                    pagesize=(11, 8.5))
    
    # Assertions
    assert mock_figure_canvas.called
    assert pdf.savefig.called
    assert mock_canvas_instance.draw.called

    # Ensure that the figure was cleared for each new table
    assert mock_canvas_instance.figure.clear.call_count == 2

    # Verify colors in draw_as_table calls
    ax = mock_canvas_instance.figure.gca()
    the_table = ax.tables[0]
    nrows, ncols = len(data) // 2 + 1, len(data.columns)

    # Mock the table
    setup_mock_table(the_table, nrows, ncols, 'lightblue', 'lightblue', [
        ['white', 'white'],
        ['lightgray', 'lightgray'],
        ['white', 'white'],
    ])

    # Verify row colors
    for row in range(1, nrows):
        assert the_table.get_celld()[(row, -1)].get_facecolor() == 'lightblue'
    
    # Verify column colors
    for col in range(ncols):
        assert the_table.get_celld()[(0, col)].get_facecolor() == 'lightblue'
    
    # Verify alternating cell colors
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
