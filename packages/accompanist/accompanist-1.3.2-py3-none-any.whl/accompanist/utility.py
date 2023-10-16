import re
import ast
import sys


def colorize_print(message: str, color: str) -> None:
    color_dic = {"red": "31m",
                 "green": "32m",
                 "yellow": "33m",
                 "blue": "34m",
                 "purple": "35m",
                 "cyan": "36m"}
    print("\033[" + color_dic[color] + message + "\033[0m")

def extract_path(path: str) -> str:
    if len(path) > 52:
        path = path[:52] + "..."
    return path

def extract_user_agent(target_ua: list) -> str:

    def _split_with_comma(ua: str) -> str:
        if len(ua) > 20:
            ua = ua[:20]

        extracted_user_agent = re.split('[ ,]', ua)
        if len(extracted_user_agent) > 0:
            return extracted_user_agent[0]
        else:
            return ua

    user_agent = "NaN"
    for i in range(len(target_ua)):
        if (
            target_ua[i]["name"] == "user-agent"
            or target_ua[i]["name"] == "User-agent"
            or target_ua[i]["name"] == "User-Agent"
        ):
            user_agent = _split_with_comma(str(target_ua[i]["value"]))
    return user_agent

def extract_rule_id(rule_group_list: list) -> str:
    rule_id = "Unknown Data"
    for i in range(len(rule_group_list)):
        if rule_group_list[i]["terminatingRule"] is not None:
            rule_id = rule_group_list[i]["terminatingRule"]["ruleId"]
    return rule_id

def extract_rule_id_2(rule_group_list: list, rule_group: str) -> str:
    rule_id = "Unknown Data"
    prefix = rule_group.find("-")
    if prefix != -1:
        rule_name = rule_group[prefix+1:]
    else:
        rule_name = rule_group
    for i in range(len(rule_group_list)):
        if rule_group_list[i]["terminatingRule"] is not None:
            if rule_name in rule_group_list[i]["ruleGroupId"]:
                rule_id = rule_group_list[i]["terminatingRule"]["ruleId"]
    return rule_id

def extract_rule_group(rule_group_all_string: str) -> str:
    if rule_group_all_string.startswith("AWS") is False:
        match = re.search(r'rulegroup/(.*)/', rule_group_all_string)
        if match:
            result = match.group(1)
        return result
    else:
        return rule_group_all_string

def is_valid_days(start: int, end: int) -> None:
    _days = int(end) - int(start)
    if _days <= (40 * 24 * 3600):
        pass
    else:
        error_days = "Error: The number of days exceeds 40."
        colorize_print(error_days, "red")
        sys.exit()


def remove_sensitives_for_cwl(asis_log):
    patterns = [
        (r'{\"name\":\"authorization\",\"value\":\".*?\"}', '{\"name\":\"authorization\",\"value\":\"*** Redacted ***\"}'),
        (r'{\"name\":\"Authorization\",\"value\":\".*?\"}', '{\"name\":\"Authorization\",\"value\":\"*** Redacted ***\"}'),
        (r'{\"name\":\"cookie\",\"value\":\".*?\"}', '{\"name\":\"cookie\",\"value\":\"*** Redacted ***\"}'),
        (r'{\"name\":\"Cookie\",\"value\":\".*?\"}', '{\"name\":\"Cookie\",\"value\":\"*** Redacted ***\"}')
    ]

    redacted_log = str(asis_log)
    for before, after in patterns:
        redacted_log = re.sub(before, after, redacted_log)

    return ast.literal_eval(redacted_log)


def remove_sensitives_for_s3(asis_log):
    patterns = [
        (r'{\"name\":\"authorization\",\"value\":\".*?\"}', '{"name":"authorization","value":"*** Redacted ***"}'),
        (r'{\"name\":\"Authorization\",\"value\":\".*?\"}', '{"name":"Authorization","value":"*** Redacted ***"}'),
        (r'{\"name\":\"cookie\",\"value\":\".*?\"}', '{"name":"cookie","value":"*** Redacted ***"}'),
        (r'{\"name\":\"Cookie\",\"value\":\".*?\"}', '{"name":"Cookie","value":"*** Redacted ***"}')
    ]

    redacted_log = str(asis_log)
    for before, after in patterns:
        redacted_log = re.sub(before, after, redacted_log)

    return redacted_log

