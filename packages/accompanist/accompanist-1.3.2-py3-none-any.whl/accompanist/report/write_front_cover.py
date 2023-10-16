
import datetime
import site

import matplotlib.lines as lines
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image

import accompanist.version as ve

LOGO_FILE: str = "logo_trans.png"


def write_front_cover(fig: Figure, color: str) -> None:
    """
    Write the cover of the analysis report
    """
    fig.add_artist(lines.Line2D([0, 1], [0.24, 0.24], color=color, linewidth=306, zorder=0))

    title_1: str = "AWS WAF Log"
    title_2: str = "Analysis Report"
    today: datetime.date = datetime.date.today()
    creation_date: str = "Creation Date: " + str(today)
    description: str = "This report was automatically generated with"

    fig.text(0.1, 0.80, title_1, color="#000000", fontsize=50, fontweight="bold")
    fig.text(0.1, 0.66, title_2, color="#000000", fontsize=50, fontweight="bold")
    fig.text(0.7, 0.52, creation_date, color="#757575", fontsize=18, fontweight="bold")
    fig.text(0.262, 0.3, description, color="#ffffff", fontsize=18)
    fig.text(0.44, 0.05, "Version: " + ve.VERSION, color="#ffffff", fontsize=16, fontweight="bold")

    try:
        # Display Logo
        logo_location: str = "".join(site.getsitepackages()) + "/accompanist/resource/" + LOGO_FILE
        log_image = Image.open(logo_location)
        bbox={"edgecolor": "none", "facecolor": color}
        ax = fig.subplots()
        ab = AnnotationBbox(OffsetImage(log_image, zoom=0.7, alpha=1.0), (0.45, 0.08), bboxprops=bbox)
        ax.add_artist(ab)
        ax.axis('off')
    except:
        pass

