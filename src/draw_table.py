import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from matplotlib.backends.backend_pdf import PdfPages

def _draw_as_table(df, pagesize, rowlabels):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
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
    return fig
 
def plot_data_table(data, pdf, rowlabels, numpages=(1, 1), pagesize=(11, 8.5)):
    nh, nv = numpages
    rows_per_page = len(data) // nh
    cols_per_page = len(data.columns) // nv
    for i in range(0, nh):
        for j in range(0, nv):
            pagelabels = rowlabels[(i*rows_per_page):min((i+1)*rows_per_page, len(rowlabels))]
            page = data.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(data)),
                           (j*cols_per_page):min((j+1)*cols_per_page, len(data.columns))]
            fig = _draw_as_table(page, pagesize, pagelabels)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
