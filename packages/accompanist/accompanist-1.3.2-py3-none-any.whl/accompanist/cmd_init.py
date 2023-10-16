import json

import click

import accompanist.utility as ut

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(name="init", context_settings=CONTEXT_SETTINGS,
               help="Configure the accompanist's initial settings.")
@click.option("-l", "--log-destination", required=True, default="CWL",
              type=click.Choice(["CWL", "S3"]),
              prompt="Please select a log destination type",
              help="Select a log destination type of AWS WAF.")
@click.option("-d", "--destination-name", required=True, default="aws-waf-logs-xxxxxxx", type=str,
              prompt="Please input a log destination name, CloudWatch Logs log group name or S3 bucket name.",
              help="Set a log destination name of AWS WAF, CloudWatch Logs log group name or S3 bucket name.")
@click.option("-p", "--path", required=True, default="/.env", type=str,
              prompt="Please input a analysis target URI path",
              help="Set a URI path for counts that is blocked/counted.")
@click.option("-c", "--comment", required=True,
              default="This is a sample comment.", type=str,
              prompt="Please input a comment on the report",
              help="Set a comment for report.")
def init(log_destination: str, destination_name: str, path: str, comment: str) -> None:

    configure_items = {
        "log_destination": log_destination,
        "destination_name": destination_name,
        "target_uri": [path],
        "comment": [comment]
    }

    with open("config.json", mode="w", encoding="utf-8") as f:
        json.dump(configure_items, f, indent=2)

    info_config = "\n[Info] A configuration file \"config.json\" is generated!"
    info_omitted = "[Info] The other path names and comment can also be added optionally by editing that file. They were omitted in this automatically initialized process.\n"
    ut.colorize_print(info_config, "cyan")
    ut.colorize_print(info_omitted, "cyan")
