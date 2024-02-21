import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


def draw_as_table(df, title, rowlabels, canvas):
    canvas.figure.clear()
    alternating_colors = [
        ['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    ax = canvas.figure.subplots()
    ax.axis('off')
    ax.set_title(title)
    the_table = ax.table(cellText=df.values,
                         colLabels=df.columns,
                         rowLabels=rowlabels,
                         rowColours=['lightblue']*len(df),
                         colColours=['lightblue']*len(df.columns),
                         cellColours=alternating_colors,
                         cellLoc='center',
                         loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(6)

    canvas.draw()


def plot_data_table(data, pdf, rowlabels, title,
                    numpages=(1, 1), pagesize=(11, 8.5)):
    nh, nv = numpages
    rows_per_page = len(data) // nh
    cols_per_page = len(data.columns) // nv + 1
    fig, _ = plt.subplots(figsize=pagesize)
    canvas = FigureCanvasQTAgg(fig)
    for i in range(0, nh):
        for j in range(0, nv):
            pagelabels = rowlabels[(i*rows_per_page):min(
                (i+1)*rows_per_page, len(rowlabels))]
            page = data.iloc[(i*rows_per_page):min((i+1)*rows_per_page,
                             len(data)),
                             (j*cols_per_page):min((j+1)*cols_per_page,
                             len(data.columns))]
            draw_as_table(page, title, pagelabels, canvas)
            pdf.savefig(canvas.figure, bbox_inches='tight')

    plt.close(canvas.figure)
