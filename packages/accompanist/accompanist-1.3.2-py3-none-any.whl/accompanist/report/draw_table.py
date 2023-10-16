import json

import numpy as np
from matplotlib.figure import Figure
from pandas.core.frame import DataFrame

import accompanist.utility as ut

CONFIG_FILE = "config.json"


def draw_table(waf_log: DataFrame, fig: Figure) -> None:
    """
    Draw a table
    """
    TABLE_TITLE = "Requests Matched Specific Paths"
    uri_data = calc_count_of_uris(waf_log)

    fig.subplots_adjust(top=0.64, left=0.04, right=0.82, hspace=0)
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")
    ax.set_title(TABLE_TITLE, loc="left", y=1.17, x=0.07, fontsize="20",
                 fontweight="bold", color="black")

    col_labels = ["No.", "Path Name", "Total Count"]
    col_widths = [0.1, 0.6, 0.2]
    col_colors = ["#3d3d3d", "#3d3d3d", "#3d3d3d"]

    cell_colors = np.full_like(uri_data, "", dtype=object)
    for i in range(len(uri_data)):
        if i % 2 == 0:
            for j in range(3):
                cell_colors[i, j] = "#FFFFFF"
        else:
            for j in range(3):
                cell_colors[i, j] = "#F2F2F2"

    uri_table = ax.table(cellText=uri_data,
                         cellColours=cell_colors,
                         colLabels=col_labels,
                         colColours=col_colors,
                         colWidths=col_widths,
                         colLoc="center",
                         loc="upper left",
                         bbox=[0.1, 0.1, 0.9, 1.0]
                         )
    # Cell Height contol
    cellDict = uri_table.get_celld()
    for j in range(0, len(col_labels)):
        cellDict[(0, j)].set_height(1.2)
        for i in range(1, len(uri_data) + 1):
            cellDict[(i, j)].set_height(1)

    for i in range(1, len(uri_data) + 1):
        uri_table[i, 0]._text.set_horizontalalignment("center")
        uri_table[i, 1]._text.set_horizontalalignment("left")
        uri_table[i, 2]._text.set_horizontalalignment("right")

    for j in range(0, 3):
        uri_table[0, j]._text.set_color("white")

    for i in range(0, len(uri_data)):
        if uri_data[i][2] != "":
            if int(uri_data[i][2]) >= 10:
                uri_table[i + 1, 2]._text.set_color("#F30100")
            elif int(uri_data[i][2]) >= 1:
                uri_table[i + 1, 2]._text.set_color("#F47A55")

    uri_table.auto_set_font_size(False)
    uri_table.set_fontsize(18)

    for key, cell in uri_table.get_celld().items():
        cell.set_linewidth(2)
        cell.set_edgecolor("white")

    note = "[Note] The total count is inaccurate if the COUNT action is chosen because one or more rules may count some requests."
    ax.text(0.1, 0.01, note, color="black", fontsize=12)


def calc_count_of_uris(waf_log: DataFrame) -> list:
    """
    Count the number of URIs
    """

    f = open(CONFIG_FILE, "r")
    settings_file = json.load(f)
    f.close()

    uris: list = settings_file["target_uri"]
    counted_uris: list = []
    index: int = 0
    for uri in uris:
        count: int = 0
        index = index + 1
        if index <= 12:
            if uri in waf_log["uri"].values:
                count = waf_log.groupby("uri").get_group(uri)["uri"].count()
            counted_uris.append([index, uri, count])
        else:
            warning_path = "[Warning] Some paths can't be shown because the number of paths may be exceeded."
            ut.colorize_print(warning_path, "yellow")
            exit

    if len(uris) < 12:
        index = len(uris)
        for i in range(12 - len(uris)):
            index = index + 1
            counted_uris.append([index, "", ""])

    return (counted_uris)
