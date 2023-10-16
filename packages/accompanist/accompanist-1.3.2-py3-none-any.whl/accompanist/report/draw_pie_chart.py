import matplotlib.lines as lines
import pandas as pd
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
from pandas.core.frame import DataFrame
from pandas.core.series import Series


class CalcTop5Class:
    def __init__(self) -> None:
        pass

    def count_top5(self, target_row: Series) -> Series:
        """
        Calculate top 5 data
        """
        self._data: Series = target_row.value_counts(sort=True) / target_row.value_counts().sum() * 100
        self._top5: Series = self._data[:5]
        self._dropped: Series = self._data.drop(self._top5.index)

        # Display "Others" if the remain is not 0
        if self._dropped.shape[0] > 0:
            self._top5["[Others]"] = pd.Series(self._dropped[0:].sum(), dtype="float64").to_string(index=False)

        return self._top5


class DrawpieChartClass:
    def __init__(self) -> None:
        self._colors: list = ["#2466a9", "#3f86bf", "#609fc6", "#88b5ce", "#bcd4e5", "#B2B2B2"]  # Blue palette
        self._wedgeprops: dict = {"alpha": 0.9, "edgecolor": "white", "linewidth": 1, "width": 0.7}
        self._textprops: dict = {"weight": "bold", "color": "#ffff00", "fontsize": "14"}

    def pie_chart(self, ax: Axes, data: Series, title: str) -> None:
        """
        Draw pie chart
        """
        ax.pie(data, colors=self._colors, startangle=90, counterclock=False,
               labels=data.index, pctdistance=0.7,
               autopct=lambda p: "{: .0f}%".format(p) if p >= 3 else "",
               wedgeprops=self._wedgeprops, textprops=self._textprops, labeldistance=None)
        ax.legend(loc="upper left", bbox_to_anchor=(1.3, 0.94),
                  prop={"size": "16", "weight": "bold"}, frameon=False, ncol=1)
        ax.set_title(title, loc="left", pad=10, fontsize="20", fontweight="bold", color="black")


def draw_pie_chart(waf_log_df: DataFrame, fig_a: Figure, fig_b: Figure, fig_c: Figure, mask_ip: bool) -> None:
    """
    Draw pie chart for top 5
    """
    top5: list = [0] * 6

    calc = CalcTop5Class()

    for i in range(len(top5)):
        top5[i] = calc.count_top5(waf_log_df.iloc[:, i + 1])

    # Masking IPs
    if mask_ip:
        top5[2] = (mask_ip_addresses(top5[2]))
    else:
        # Add country code if the number of IPs > 5
        if len(top5[2].index) > 5:
            top5[2].index = add_cc_to_ip(waf_log_df, top5)

    fig_a.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)
    fig_b.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)
    fig_c.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)

    # Add note for country code
    add_cc_notation(fig_c)

    ax_a_upper: Axes = fig_a.add_subplot(2, 1, 1)
    ax_a_lower: Axes = fig_a.add_subplot(2, 1, 2)
    ax_b_upper: Axes = fig_b.add_subplot(2, 1, 1)
    ax_b_lower: Axes = fig_b.add_subplot(2, 1, 2)
    ax_c_upper: Axes = fig_c.add_subplot(2, 1, 1)
    ax_c_lower: Axes = fig_c.add_subplot(2, 1, 2)

    ax_a_upper.set_position([0.004, 0.42, 0.4, 0.3])
    ax_a_lower.set_position([0.004, 0.06, 0.4, 0.3])
    ax_b_upper.set_position([0.004, 0.42, 0.4, 0.3])
    ax_b_lower.set_position([0.004, 0.06, 0.4, 0.3])
    ax_c_upper.set_position([0.004, 0.42, 0.4, 0.3])
    ax_c_lower.set_position([0.004, 0.06, 0.4, 0.3])

    draw = DrawpieChartClass()

    draw.pie_chart(ax_a_upper, top5[0], "Rule Group")
    draw.pie_chart(ax_a_lower, top5[5], "Rule")
    draw.pie_chart(ax_b_upper, top5[1], "Path Name")
    draw.pie_chart(ax_b_lower, top5[4], "User Agent")
    draw.pie_chart(ax_c_upper, top5[2], "IP Address")
    draw.pie_chart(ax_c_lower, top5[3], "Country")


def mask_ip_addresses(ip_dataframe: Series) -> Series:
    """
    Mask IP adress if the option was set
    """
    masked_ips: list = []
    for i in range(len(ip_dataframe)):
        ip_segments: list = str(ip_dataframe.index[i]).split(".")
        if i != 5:
            ip_segments[0] = "xxx"
            ip_segments[1] = "xxx"
        masked_ip: str = '.'.join(ip_segments)
        masked_ips.append(masked_ip)
    ip_dataframe.index = [masked_ips[0], masked_ips[1], masked_ips[2],
                          masked_ips[3], masked_ips[4], masked_ips[5]]
    return ip_dataframe

def add_cc_notation(fig_b: Figure) -> None:
    """
    Add country code next to IPs
    """
    fig_b.add_artist(lines.Line2D([0.66, 0.93], [0.16, 0.16], color="#eeeeee", linewidth=60, zorder=0))
    CC_NOTE: str = "Please refer to the following for the country code."
    CC_LINK: str = "https://en.wikipedia.org/wiki/ISO_3166-2"
    fig_b.text(0.64, 0.17, CC_NOTE, fontsize=12, ha="left")
    fig_b.text(0.64, 0.13, CC_LINK, fontsize=12, ha="left", color="blue",
               url="https://en.wikipedia.org/wiki/ISO_3166-2")

def add_cc_to_ip(waf_log_df: DataFrame, top5: Series) -> list:
    country: str = ""
    old_index: list = top5[2].index.tolist()
    new_index: list = []
    for i in range(len(top5[2].index)):
        if top5[2].index[i] != "[Others]":
            for index, row in waf_log_df.iterrows():
                if top5[2].index[i] in row["ip"]:
                    country = row["country"]
                    break
            new_index.append(old_index[i] + "  (" + country + ")")

    if len(top5[2].index) >= 5:
        last_index = len(top5[2].index) - 1
        new_index.append(old_index[last_index])
    return new_index

