import datetime

import numpy as np
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
from numpy import int64, ndarray
from pandas.core.frame import DataFrame
from pandas.core.series import Series


class DrawHistgramClass:
    def __init__(self) -> None:
        self._hours = 3
        self._bins = 0
        self._label_and_count = ""
        self._xlocation: list = []
        self._all_xlocation: ndarray
        self._xlabel: list = []
        self._1day_seconds = 3600 * 24 * 1000
        self._xlabel_threshold = 0

    def histgram(self, ax: Axes, time: Series, target: Series,
                 label: str, color: str, utc_offset: int, y_limit_str: str) -> None:
        """
        Create settings for histgram
        """
        self._calc_xticks_and_labels(time[0], time[len(time) - 1], utc_offset)
        self._bins = int((self._last_xlocation - self._first_xlocation - self._1day_seconds)
                         / 1000 / (3600 * self._hours)) + 8  # margin = 8
        self._label_and_count = label + " (" + str(len(target)) + ")"
        ax.grid(True)
        # ax.yaxis.grid(False)
        y_limit = int(y_limit_str)
        ax.set_ylim(0, y_limit)
        if y_limit >= 50:
            if label != "Third Party":  # a hack for preventing from drawing twice
                ax.axhspan(y_limit / 5 * 1, y_limit / 5 * 2, color="gray", alpha=0.05)
                ax.axhspan(y_limit / 5 * 3, y_limit / 5 * 4, color="gray", alpha=0.05)
        ax.hist(target, alpha=0.7, bins=self._bins, range=(self._first_xlocation, self._last_xlocation),
                label=self._label_and_count, color=color, edgecolor="white", linewidth=0)
        ax.legend(loc="upper left", prop={"size": 12}, fancybox=True,
                  edgecolor="gray", facecolor="white", framealpha=1)

        ax.set_xticks(self._xlocation)
        ax.set_xticklabels(self._xlabel)
        ax.tick_params(labelsize=10, direction = "in", length=0)

    def _calc_xticks_and_labels(self, end_time: int64, start_time: int64, utc_offset: int) -> None:
        tz_offset = 3600 * 1000 * utc_offset
        self._last_xlocation = end_time - end_time % (self._1day_seconds) + self._1day_seconds - tz_offset
        self._first_xlocation = start_time - start_time % (self._1day_seconds) - tz_offset
        self._number_of_labels = int((self._last_xlocation - self._first_xlocation) / self._1day_seconds) + 1
        self._all_xlocation = np.linspace(self._last_xlocation, self._first_xlocation, self._number_of_labels, dtype=int)

        self._xlabel_threshold = int(self._number_of_labels / 5) if (int(self._number_of_labels / 5)) > 2 else 2

        self._xlocation = []
        if self._number_of_labels > 7:
            for i in range(len(self._all_xlocation)):
                if (i % self._xlabel_threshold == 1):
                    self._xlocation.append(self._all_xlocation[i])
        else:
            self._xlocation = list(self._all_xlocation)

        self._xlabel = []
        for i in range(len(self._xlocation)):
            self._xlabel.append(datetime.datetime
                                .fromtimestamp(self._xlocation[i] / 1000.0)
                                .strftime("%m/%d(%a) %H:%M"))


def draw_histgram(waf_log: DataFrame, fig: Figure, utc_offset: int, y_limit: str) -> None:
    """
    Draw two histgrams
    """
    TITLE_OF_TOTAL = "Blocked/Counted Request"
    TITLE_OF_RULES = "Breakdown by Rule Provider"

    fig.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)
    ax_1 = fig.add_subplot(2, 1, 1)
    ax_2 = fig.add_subplot(2, 1, 2)

    ax_1.set_position([0.099, 0.506, 0.8, 0.2])
    ax_2.set_position([0.099, 0.14, 0.8, 0.2])

    ax_1.set_title(TITLE_OF_TOTAL, loc="left", pad=18, fontsize="20", fontweight="bold", color="black")
    ax_2.set_title(TITLE_OF_RULES, loc="left", pad=18, fontsize="20", fontweight="bold", color="black")

    aws_managed = waf_log[waf_log.rule.str.match('^AWS')]
    third_party = waf_log[waf_log.rule.str.match('^(?!AWS)')]

    draw = DrawHistgramClass()

    draw.histgram(ax_1, waf_log["time"], waf_log["time"], "Total", "gray", utc_offset, y_limit)
    draw.histgram(ax_2, waf_log["time"], aws_managed["time"], "AWS", "indianred", utc_offset, y_limit)
    draw.histgram(ax_2, waf_log["time"], third_party["time"], "Third Party", "skyblue", utc_offset, y_limit)

    fig.text(0.38, 0.460, "Date and Time [bin-width: 3 hours]", fontsize=12, ha="left", weight="bold")
    fig.text(0.38, 0.096, "Date and Time [bin-width: 3 hours]", fontsize=12, ha="left", weight="bold")
