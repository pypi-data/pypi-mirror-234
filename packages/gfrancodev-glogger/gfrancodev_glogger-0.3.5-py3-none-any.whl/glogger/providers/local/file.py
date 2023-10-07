from os import environ
from colorama import Fore
from sys import exit
import logging
from datetime import datetime
from glogger.base.client import Client


class FileLogger(Client):
    def __init__(self):
        log_file_path = environ.get("LOG_FILE_PATH", "glogger.log")
        logging.basicConfig(filename=log_file_path, level=logging.INFO)

    def send(self, data):
        try:
            current_time = datetime.utcnow().isoformat()
            log_message = f"{current_time} - {str(data)}"
            logging.info(str(log_message))
            print(f"""{Fore.BLUE}[LOCAL] ➡️ {str(log_message)}""")
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failure to record information in the log file.
            """
            )
            exit(1)
