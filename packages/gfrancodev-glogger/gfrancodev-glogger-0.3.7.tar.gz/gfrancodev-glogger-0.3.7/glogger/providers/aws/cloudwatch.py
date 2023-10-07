import os
from boto3 import client
from time import time, sleep
from colorama import Fore
from sys import exit
from glogger.base.client import Client


class CloudWatch(Client):
    def __init__(self):
        self.region = str(os.getenv("AWS_DEFAULT_REGION"))
        self.hostname = str(os.getenv("HOSTNAME"))
        self.stream_name = str(os.getenv("AWS_CLOUDWATCH_LOG_STREAM_NAME"))
        self.aws_access_key_id = str(os.getenv("AWS_ACCESS_KEY_ID"))
        self.aws_secret_access_key = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
        self.log_group_name = str(os.getenv("AWS_CLOUDWATCH_LOG_GROUP_NAME"))
        self.log_stream_name = f'{self.stream_name + self.hostname}'
        self.cw_client = client(
            "logs",
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        self.send("starting glogger")

    def send(self, data):
        sleep(0.1)
        try:
            self.cw_client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[{"timestamp": int(time() * 1000), "message": data or "void" }],
            )

            print(f"""{Fore.BLUE}[AWS_CLOUDWATCH] ➡️ {data}""")
        except self.cw_client.exceptions.ResourceNotFoundException:
            try:
                self.cw_client.create_log_group(logGroupName=self.log_group_name)
                print(
                    f"""
                            {Fore.YELLOW} ⚠️ Your log group didn't exist, we created it for you!
                            Log group created:{Fore.RESET} {Fore.LIGHTYELLOW_EX}{self.log_group_name}{Fore.RESET}
                            """
                )
            except self.cw_client.exceptions.ResourceAlreadyExistsException:
                print(
                    f"""
                            {Fore.YELLOW} ⚠️ Your stream of logs didn't exist, we created it for you!
                            Stream of logs:{Fore.RESET} {Fore.LIGHTYELLOW_EX}{self.log_stream_name}{Fore.RESET}
                            """
                )
                self.cw_client.create_log_stream(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name,
                )
                pass
            finally:
                self.cw_client.put_log_events(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name,
                    logEvents=[
                        {"timestamp": int(time() * 1000), "message": data}
                    ],
                )
                print(
                    f"""
                        {Fore.BLUE}[AWS_CLOUDWATCH] ➡️ {data}
                        """
                )
        except BaseException as error:
            print(
                f"""
                {Fore.RED} ❌ Failed to connect to client CloudWatch 2.
                """
            )
            exit(1)
