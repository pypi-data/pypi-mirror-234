import os
import random
import subprocess
import sys
import platform

import click
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages as pp

import accompanist.report.draw_histgram as dh
import accompanist.report.draw_pie_chart as dp
import accompanist.report.draw_table as dt
import accompanist.report.write_comment as wc
import accompanist.report.write_front_cover as wf
import accompanist.report.write_header_footer as wh
import accompanist.utility as ut

INPUT_CSV_FILE = "waf-log.csv"
OUTPUT_PDF_FILE = "report.pdf"
A4_SIZE = (11.69, 8.27)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(name="play", context_settings=CONTEXT_SETTINGS,
               help="Analyze WAF logs and generate a report.")
@click.option("-c", "--colorful", required=False, is_flag=True,
              help="Set a random color of report theme (instead of color).")
@click.option("-d", "--color", required=False, type=str,
              help="Customize a color of report theme with color code,  (e.g.) #cccccc.")
@click.option("-m", "--mask-ip", required=False, is_flag=True,
              help="Mask IP addresses on pie chart.")
@click.option("-u", "--utc-offset", required=False, type=int, default=9,
              help="Set a number of UTC offest. The defaut offset is UTC+9 (Asia/Tokyo).")
@click.option("-y", "--y-limit", required=False, default="50",
              type=click.Choice(["10", "20", "30", "50", "100", "500", "1000"]),
              help="Adjust a Y-axis max limitation for histograms due to many requests.")
@click.option("-er", "--exclude-rule-group", required=False, type=str,multiple=True,
              help="Exclude a rule group (or multiple rule groups) from analysis target.")
def play(color: str, colorful: str, mask_ip: bool, utc_offset: int, y_limit: str,
         exclude_rule_group: str) -> None:

    # Pre-Process
    if os.path.isfile(INPUT_CSV_FILE):
        if os.stat(INPUT_CSV_FILE).st_size != 0:
            waf_log = pd.read_csv(INPUT_CSV_FILE, header=None)
            waf_log.columns = ["time", "rule", "uri", "ip", "country", "ua", "ruleid"]
            waf_log = waf_log[~waf_log["rule"].isin(exclude_rule_group)]
            waf_log.reset_index(drop=True, inplace=True)
        else:
            error_empty = "[Error] A WAF log CSV file, " + INPUT_CSV_FILE + " is empty."
            ut.colorize_print(error_empty, "red")
            sys.exit()
    else:
        error_log = "[Error] A WAF log CSV file, " + INPUT_CSV_FILE + " is not found in the current directory."
        ut.colorize_print(error_log, "red")
        sys.exit()

    plt.rcParams["font.family"] = "Arial"
    # plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]

    fig_1 = plt.figure(figsize=A4_SIZE)
    fig_2 = plt.figure(figsize=A4_SIZE)
    fig_3 = plt.figure(figsize=A4_SIZE)
    fig_4 = plt.figure(figsize=A4_SIZE)
    fig_5 = plt.figure(figsize=A4_SIZE)
    fig_6 = plt.figure(figsize=A4_SIZE)
    fig_7 = plt.figure(figsize=A4_SIZE)

    figs = [fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7]

    color_list = ["#154f74", "#1397ab", "#9a540f",
                  "#ffa50d", "#74bd97", "#2fcdfa", "#f595ff", "#9a5bc0", "#000000"]

    if color is None:
        if colorful:
            index = random.randint(0, len(color_list) - 1)
            color = color_list[index]
            info_color = "[Info] A theme color of the report was chosen randomly: " + color
            ut.colorize_print(info_color, "cyan")
        else:
            color = "#154f74"  # Default color

    # Add front cover
    wf.write_front_cover(fig_1, color)

    # Calculation & Draw
    dh.draw_histgram(waf_log, fig_2, utc_offset, y_limit)
    dp.draw_pie_chart(waf_log, fig_3, fig_4, fig_5, mask_ip)
    dt.draw_table(waf_log, fig_6)
    wc.write_comment(fig_7)

    # Post-Process
    wh.write_header_and_footer(waf_log["time"], figs[1:], utc_offset, color)

    pdf = pp(OUTPUT_PDF_FILE)

    for i in figs:
        pdf.savefig(i)

    pdf.close()

    if platform.system() == "Darwin":
        subprocess.Popen("open " + OUTPUT_PDF_FILE, shell=True)
    else:
        report_created = "The report file, \"report.pdf\" is generated."
        ut.colorize_print(report_created, "purple")

