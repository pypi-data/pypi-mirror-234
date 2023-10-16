import csv
import datetime
import json
import os
import sys
import time
import threading
import itertools

import boto3
import click

import accompanist.utility as ut

CONFIG_FILE = "config.json"
SHEET_MUSIC_FILE = "sheet_music.json"
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(name="listen", context_settings=CONTEXT_SETTINGS,
               help="Get a WAF log file in CSV format.")
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
def listen(days: int, start_time: int, end_time: int, action: str, json_log: bool) -> None:

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

    log_group = config_dict["destination_name"]
    client = boto3.client("logs")

    if action == "BLOCK":
        query = 'fields @timestamp, @message | filter @message like "BLOCK" | sort @timestamp desc'
    elif action == "COUNT":
        query = 'fields @timestamp, @message | filter @message like /"action":"COUNT"/ | sort @timestamp desc'
    elif action == "EXCLUDED_AS_COUNT":
        query = 'fields @timestamp, @message | filter @message like "EXCLUDED_AS_COUNT" | sort @timestamp desc'
    else:
        error_action = "[Error] The action is empty or invalid. You should set BLOCK or COUNT"
        ut.colorize_print(error_action, "red")
        sys.exit()

    if days is not None and (start_time is None or end_time is None):
        end_time = int(time.time())
        start_time = end_time - days * 24 * 3600
    else:
        days_warning = "[Warning] The inputted number of days is ignored as the start & end times had been set."
        ut.colorize_print(days_warning, "yellow")

    ut.is_valid_days(start_time, end_time)

    try:
        start_query_response = client.start_query(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time,
            queryString=query,
            limit=10000
        )
    except Exception as e:
        error_query = "[Error] An Error occurred just after the CWL Logs Insights query started"
        ut.colorize_print(error_query, "red")
        raise e

    asis_response = None
    info_start = "[Info] A CloudWatch Logs Insights query started."
    ut.colorize_print(info_start, "cyan")

    # Start spinner animation
    spinner_flag_completed = False
    t = threading.Thread(target=_spin_animation)
    t.start()

    while asis_response is None or asis_response["status"] == "Running":
        time.sleep(3)
        # print(" ... ... ... ")
        try:
            asis_response = client.get_query_results(queryId=start_query_response["queryId"])
        except Exception as e:
            error_get = "[Error] An Error occurred just after the command issued to get query results"
            ut.colorize_print(error_get, "red")
            raise e

    # Stop spinner animation
    spinner_flag_completed = True
    time.sleep(1)

    info_complete = "[Info] The query has been completed!"
    ut.colorize_print(info_complete, "cyan")

    # Remove several items from the header to prevent information leakage.
    response = ut.remove_sensitives_for_cwl(asis_response)

    if json_log:
        # Outputting a log for debug
        # with open("raw-log.json", mode="w", encoding="utf-8") as f:
            # json.dump(response, f, indent=4)

        log_json = []
        for i in range(len(response["results"])):
            log_json.append(response["results"][i][1]["value"])

        with open("waf-log.json", mode="w", encoding="utf-8") as f:
            log_str = "[" + str(', '.join(log_json)) + "]"
            json.dump(json.loads(log_str), f, indent=2)

        debug_message = "[Important] A JSON log file is generated. And please handle it with care!"
        ut.colorize_print(debug_message, "purple")

    with open("waf-log.csv", mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, lineterminator="\n",  delimiter="\t", escapechar="\\")

        if action == "BLOCK":
            for i in range(len(response["results"])):
                message = json.loads(response["results"][i][1]["value"])
                if message["action"] == "BLOCK": # to distinguish in logs. it's only for CWL
                    row = str(message["timestamp"]) + "," + \
                        message["terminatingRuleId"] + "," + \
                        message["httpRequest"]["uri"] + "," + \
                        message["httpRequest"]["clientIp"] + "," + \
                        message["httpRequest"]["country"] + "," + \
                        ut.extract_user_agent(message["httpRequest"]["headers"]) + "," + \
                        ut.extract_rule_id(message["ruleGroupList"])
                    writer.writerow([row])
        elif action == "COUNT":
            for i in range(len(response["results"])):
                message = json.loads(response["results"][i][1]["value"])
                for j in range(len(message["nonTerminatingMatchingRules"])):
                    row = str(message["timestamp"]) + "," + \
                        message["nonTerminatingMatchingRules"][j]["ruleId"] + "," + \
                        ut.extract_path(message["httpRequest"]["uri"]) + "," + \
                        message["httpRequest"]["clientIp"] + "," + \
                        message["httpRequest"]["country"] + "," + \
                        ut.extract_user_agent(message["httpRequest"]["headers"]) + "," + \
                        ut.extract_rule_id_2(message["ruleGroupList"],
                                             message["nonTerminatingMatchingRules"][j]["ruleId"]
                                             )
                    writer.writerow([row])
        elif action == "EXCLUDED_AS_COUNT":
            for i in range(len(response["results"])):
                message = json.loads(response["results"][i][1]["value"])
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
        "log_destination": "CWL",
        "destination_name": log_group,
    }
    with open(SHEET_MUSIC_FILE, mode="w", encoding="utf-8") as f:
        json.dump(sheet_music, f, indent=2)
    info_sheet = "[Info] A " + SHEET_MUSIC_FILE + " file was created for analysis."
    ut.colorize_print(info_sheet, "cyan")
