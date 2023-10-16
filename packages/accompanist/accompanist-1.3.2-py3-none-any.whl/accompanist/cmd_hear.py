import csv
import datetime
import gzip
import io
import json
import operator
import os
import re
import sys
import time
import itertools
import threading

import boto3
import click

import accompanist.utility as ut

CONFIG_FILE = "config.json"
SHEET_MUSIC_FILE = "sheet_music.json"
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(name="hear", context_settings=CONTEXT_SETTINGS,
               help="Get WAF log files in CSV format from S3 bucket.")
@click.option("-a", "--action", required=True, default="BLOCK",
              prompt="Please input the action of AWS WAF",
              type=click.Choice(["BLOCK", "COUNT", "EXCLUDED_AS_COUNT"]),
              help="Chose an action type of AWS WAF. The default is \"BLOCK\".")
@click.option("-d", "--days", required=False, type=int, default="1",
              prompt="Please input the number of analysis target days",
              help="Set a number of the past days until today for analysis target period.")
@click.option("-s", "--start_time", required=False, type=int,
              help="Set a UNIX time of the oldest time for analysis target period (instead of \"--days\").")
@click.option("-e", "--end_time", required=False, type=int,
              help="Set a UNIX time of the latest time for analysis target period (instead of \"--days\").")
@click.option("-j", "--json_log", required=False, is_flag=True,
              help="Output a JSON log file. Please handle it with care.")
def hear(days: int, start_time: int, end_time: int, action: str, json_log: bool) -> None:

    def is_target_term(target_key: str, date_list: list) -> bool:
        is_term = False
        for date in date_list:
            if re.search(date, target_key):
                # print(" ... ... ...")
                # print("- " + target_key) # for debug
                is_term = True
        return is_term


    def _spin_animation():
        for spinner in itertools.cycle(['|', '/', '-', '\\']):
            if spinner_flag_completed:
                break
            sys.stdout.write("\rPlease wait... " + spinner + " ")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\rThank you for being patient.")
        print("\n")


    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, mode="r") as f:
            config_dict = json.load(f)
    else:
        error_file = "[Error] " + CONFIG_FILE + " is not found in the ccurrent directory."
        info_before = "[Info] You may have to run \"accompanist init\" at first."
        ut.colorize_print(error_file, "red")
        ut.colorize_print(info_before, "cyan")
        sys.exit()

    log_bucket = config_dict["destination_name"]
    date_list = []

    if days is not None and (start_time is None or end_time is None):
        end_time = int(time.time())
        start_time = end_time - days * 24 * 3600
    else:
        days_warning = "[Warning] The inputted number of days is ignored as the start & end times had been set."
        ut.colorize_print(days_warning, "yellow")

    ut.is_valid_days(start_time, end_time)

    for item in range(start_time, end_time + 1, 86400):
        date_list.append(time.strftime("%Y/%m/%d", time.gmtime(item)))
    print("Target Date: " + str(date_list))

    info_start = "[Info] Started downloading from S3 bucket."
    ut.colorize_print(info_start, "cyan")

    # Start spinner animation
    spinner_flag_completed = False
    t = threading.Thread(target=_spin_animation)
    t.start()

    try:
        s3 = boto3.client("s3")
        paginator = s3.get_paginator("list_objects")
        page_iterator = paginator.paginate(Bucket=log_bucket)

        # print("Downloading...")

        all_log: list = []
        for page in page_iterator:
            for obj in page["Contents"]:
                if obj["Key"].endswith("gz") and is_target_term(obj["Key"], date_list):
                    obj = s3.get_object(Bucket=log_bucket,Key=obj["Key"])
                    row = gzip.open(io.BytesIO(obj["Body"].read()), "rt").readlines()
                    for item in range(len(row)):
                        all_log.append(row[item])
    except Exception as e:
        error_query = "[Error] An Error occurred during getting logs from S3 bucket"
        ut.colorize_print(error_query, "red")
        raise e

    # Stop spinner animation
    spinner_flag_completed = True
    time.sleep(1)

    info_complete = "[Info] The downloading has been completed!"
    ut.colorize_print(info_complete, "cyan")

    log_str = "[" + str(', '.join(all_log)) + "]"
    log_json = json.loads(ut.remove_sensitives_for_s3(log_str))

    # Squeeze analysis target between start_time and end_time
    extracted_json = []
    for item in range(len(log_json)):
        timestamp = int(log_json[item]["timestamp"])
        if timestamp >= (start_time * 1000) and timestamp <= (end_time * 1000):
            extracted_json.append(log_json[item])

    if json_log:
        with open("waf-log.json", mode="w", encoding="utf-8") as f:
            json.dump(extracted_json, f, indent=2)

        debug_message = "[Important] A JSON log file is generated. And please handle it with care!"
        ut.colorize_print(debug_message, "purple")

    response = extracted_json

    with open("waf-log.csv", mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, lineterminator="\n", delimiter="\t")

        if action == "BLOCK":
            for item in range(len(response)):
                message = response[item]
                if message["action"] == "BLOCK":
                    row = str(message["timestamp"]) + "," + \
                        message["terminatingRuleId"] + "," + \
                        message["httpRequest"]["uri"] + "," + \
                        message["httpRequest"]["clientIp"] + "," + \
                        message["httpRequest"]["country"] + "," + \
                        ut.extract_user_agent(message["httpRequest"]["headers"]) + "," + \
                        ut.extract_rule_id(message["ruleGroupList"])
                    writer.writerow([row])
        elif action == "COUNT":
            for item in range(len(response)):
                message = response[item]
                for j in range(len(message["nonTerminatingMatchingRules"])):
                    if message["nonTerminatingMatchingRules"][j]["action"] == "COUNT":
                        row = str(message["timestamp"]) + "," + \
                            message["nonTerminatingMatchingRules"][j]["ruleId"] + "," + \
                            message["httpRequest"]["uri"] + "," + \
                            message["httpRequest"]["clientIp"] + "," + \
                            message["httpRequest"]["country"] + "," + \
                            ut.extract_user_agent(message["httpRequest"]["headers"]) + "," + \
                            ut.extract_rule_id_2(message["ruleGroupList"],
                                                 message["nonTerminatingMatchingRules"][j]["ruleId"]
                                                 )
                        writer.writerow([row])
        elif action == "EXCLUDED_AS_COUNT":
            for item in range(len(response)):
                message = response[item]
                for j in range(len(message["ruleGroupList"])):
                    if message["ruleGroupList"][j]["excludedRules"] is not None:
                        for k in range(len(message["ruleGroupList"][j]["excludedRules"])):
                            row = str(message["timestamp"]) + "," + \
                                ut.extract_rule_group(message["ruleGroupList"][j]["ruleGroupId"]) + "," + \
                                message["httpRequest"]["uri"] + "," + \
                                message["httpRequest"]["clientIp"] + "," + \
                                message["httpRequest"]["country"] + "," + \
                                ut.extract_user_agent(message["httpRequest"]["headers"]) + "," + \
                                message["ruleGroupList"][j]["excludedRules"][k]["ruleId"]
                            writer.writerow([row])
        else:
            error_action = "Error: action is invalid"
            ut.colorize_print(error_action, "red")
            sys.exit()

    # Reorder log items with timestamp from latest to oldest
    with open("waf-log.csv", mode="r") as f:
        csv_data = csv.reader(f, delimiter=",")
        sort_result: list = []
        sort_result = sorted(csv_data, key=operator.itemgetter(0), reverse=True)

        with open("waf-log.csv", mode="w", encoding="utf-8", newline="") as f:
            data = csv.writer(f, quoting=csv.QUOTE_NONE, lineterminator="\n", delimiter=",")
            row_item: list = []
            for row_item in sort_result:
                data.writerow(row_item)

    info_csv = "[Info] A WAF log file in CSV format was outputted."
    ut.colorize_print(info_csv, "cyan")

    # Calc dates
    s_time = datetime.datetime.fromtimestamp(start_time)
    e_time = datetime.datetime.fromtimestamp(end_time)
    days = (e_time - s_time).days

    # Dump data for creating report
    sheet_music = {
        "start_time": start_time,
        "end_time": end_time,
        "days": days,
        "action": action,
        "log_destination": "S3",
        "destination_name": log_bucket,
    }
    with open(SHEET_MUSIC_FILE, mode="w", encoding="utf-8") as f:
        json.dump(sheet_music, f, indent=2)
    info_sheet = "[Info] A " + SHEET_MUSIC_FILE + " file was created for analysis."
    ut.colorize_print(info_sheet, "cyan")



