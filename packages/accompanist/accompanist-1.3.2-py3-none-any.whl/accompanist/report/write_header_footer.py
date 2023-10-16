import datetime
import json
import site
import sys

import matplotlib.lines as lines
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from pandas.core.series import Series
from PIL import Image

import accompanist.utility as ut

LOGO_FILE: str = "logo_trans_small.png"
SHEET_MUSIC_FILE: str = "sheet_music.json"


class WriteHeaderFooterClass():
    """
    Write header and footer class
    """

    def __init__(self) -> None:

        self._dic_box = {
            "facecolor": "#757575",
            "edgecolor": "#757575",
            "boxstyle": "Round, pad=0.7",
            "linewidth": 3,
        }

    def header_footer(self, fig: Figure, page_number: str, term: str, main_color: str) -> None:
        with open(SHEET_MUSIC_FILE, mode="r") as f:
            settings_dict: dict = json.load(f)

        # Header
        page_title: str = "AWS WAF Log  (Action: " + settings_dict["action"] + ")"

        if settings_dict["log_destination"] == "CWL":
            log_dest = "Log Group"
        elif settings_dict["log_destination"] == "S3":
            log_dest = "Log Bucket"
        else:
            sys.exit()

        log_dest_name = settings_dict["destination_name"].replace("aws-waf-logs-", "")

        if len(log_dest_name) > 15:
            log_dest_name = log_dest_name[:15] + "*****"
        fig.add_artist(lines.Line2D([0, 1], [0.94, 0.94], color=main_color, linewidth=80, zorder=0))

        fig.text(0.05, 0.91, page_title, color="#ffffff", fontsize=26, fontweight="bold")
        fig.text(0.71, 0.82, log_dest + ": " + log_dest_name, color="#ffffff", fontsize=14, fontweight="bold", bbox=self._dic_box)
        fig.text(0.71, 0.76, term, color="#757575", fontsize=14)

        # Footer
        fig.add_artist(lines.Line2D([0, 1], [0.0004, 0.0004], color=main_color, linewidth=80, zorder=0))
        fig.text(0.92, 0.02, page_number, color="#949494", fontsize=20, fontweight="bold")

        # Show logo file
        try:
            logo_location: str = "".join(site.getsitepackages()) + "/accompanist/resource/" + LOGO_FILE
            log_image = Image.open(logo_location)
            bbox={"edgecolor": "none", "facecolor": main_color}
            ax_logo = fig.subplots()
            ax_logo.set_position([-0.08, 0.01, 0.8, 0.8])
            ab = AnnotationBbox(OffsetImage(log_image, zoom=0.7, alpha=1.0), (0.72, 0.03), bboxprops=bbox)
            ax_logo.add_artist(ab)
            ax_logo.axis('off')
        except:
            warning_logo: str = "[Warning] The logo file can not be shown."
            ut.colorize_print(warning_logo, "yellow")
            # raise e

def calc_term(time: Series, utc_offset: int) -> str:
    """
    Show term
    """
    with open(SHEET_MUSIC_FILE, mode="r") as f:
        settings_dict = json.load(f)

    offset = 3600 * utc_offset
    info_utc = "[Info] The current UTC offset is \"" + str(utc_offset) + "\". You can change the offset with an option, --utc-offset N."
    ut.colorize_print(info_utc, "cyan")

    oldest_time = datetime.datetime.fromtimestamp(time[len(time) - 1] / 1000.0 + offset, tz=datetime.timezone.utc).strftime("%m/%d %H:%M")
    latest_time = datetime.datetime.fromtimestamp(time[0] / 1000.0 + offset, tz=datetime.timezone.utc).strftime("%m/%d %H:%M")

    days = str(settings_dict["days"])

    if int(days) > 1:
        term = days + " days (" + oldest_time + " - " + latest_time + ")"
    else:
        term = oldest_time + " - " + latest_time
    return term


def write_header_and_footer(waf_log_time: Series, figs: Figure, utc_offset: int, color: str) -> None:
    """
    Add header and footer
    """
    term = calc_term(waf_log_time, utc_offset)

    write = WriteHeaderFooterClass()

    for fig in (figs):
        page_number = str(figs.index(fig) + 1) + " / " + str(len(figs))
        write.header_footer(fig, page_number, term, color)
