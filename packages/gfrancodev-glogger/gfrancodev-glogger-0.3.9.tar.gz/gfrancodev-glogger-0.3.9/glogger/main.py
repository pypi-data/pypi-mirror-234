#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
from sys import argv, exit
from os import environ, getcwd
from subprocess import Popen, PIPE, STDOUT
from threading import Thread, enumerate, current_thread
from glogger.base.logger import Logger
from glogger.base.client import Client
from glogger.providers.aws.cloudwatch import CloudWatch
from glogger.providers.aws.s3 import S3
from glogger.providers.google.logging import GCL
from glogger.providers.google.storage import GCS
from glogger.providers.azure.blob import AzureBlob
from glogger.providers.azure.insight import AzureApplicationInsights
from glogger.providers.local.file import FileLogger
from glogger.providers.socket.websocket import Websocket
from glogger.providers.socket.papertrail import Papertrail
from glogger.cli.command import Command
from colorama import just_fix_windows_console, init, Fore


class GLogger(Logger):
    def __init__(self, client: Client):
        self.client = client

    def watch(self, command):
        process = Popen(
            command,
            stdout=PIPE,
            stderr=STDOUT,
            universal_newlines=True,
            shell=True,
            cwd=getcwd(),
        )

        for line in process.stdout:
            self.client.send(line.strip())


def main():
    init(autoreset=True)
    just_fix_windows_console()
    Command()

    config_providers = environ.get("GLOGGER_PROVIDER", "local,aws_cloudwatch")

    log_providers = {
        "local": FileLogger(),
        "aws_cloudwatch": CloudWatch(),
        "aws_s3": S3(),
        "azure_blob": AzureBlob(),
        "azure_insight": AzureApplicationInsights(),
        "gcp_logging": GCL(),
        "gcp_storage": GCS(),
        "websocket": Websocket(),
        "papertrail": Papertrail(),
    }

    selected_providers = config_providers.split(",")
    clients = [
        log_providers[provider]
        for provider in selected_providers
        if provider in log_providers
    ]
    loggers = [GLogger(client) for client in clients]

    commands = argv[1:]

    if not commands:
        print(f"{Fore.CYAN}Usage: glogger command to watch")
        exit(1)

    for logger in loggers:
        thread = Thread(target=logger.watch, args=(commands,))
        thread.start()

    for thread in enumerate():
        if thread != current_thread():
            thread.join()


if __name__ == "__main__":
    load_dotenv()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Thread interrupted by user.")
        exit(1)
    except BaseException:
        print(f"{Fore.LIGHTRED_EX}The obersavability has been closed.")
        exit(1)