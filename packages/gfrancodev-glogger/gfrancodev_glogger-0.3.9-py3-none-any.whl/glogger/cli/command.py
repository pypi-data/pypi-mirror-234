from colorama import just_fix_windows_console, init, Fore
from sys import argv, exit
from platform import system


class Command:
    def __init__(self):
        self.version_tag = "v0.3.9"
        self.execute()

    def help(self):
        platform = system()
        global config_path

        if platform == "Linux" or platform == "Darwin":
            config_path = "/etc/glogger/glogger.config"
        if platform == "Windows":
            config_path = "C:\\ProgramData\\glogger\\glogger.config"

        help_message = (
            f"\n"
            f"        {Fore.GREEN}Usage:{Fore.RESET}\n"
            f"        glogger [command]\n"
            f"        glogger [options]\n"
            f"\n"
            f"        {Fore.GREEN}Options:{Fore.RESET}\n"
            f"        -h, --help          Display this help message\n"
            f"        -p, --providers     List available log providers\n"
            f"        -e, --env           List available enviroments for providers in the glogger.conf\n"
            f"                            the configuration file is located at: ({config_path})\n"
            f"                            \n"
            f"\n"
            f"        {Fore.MAGENTA}Explanation:{Fore.RESET}\n"
            f"        The {Fore.BLUE}'GLOGGER_CONFIG_PATH'{Fore.RESET} environment variable is essential because it loads the \n"
            f"        necessary environment variables required for the providers to function properly.\n"
            f"        \n"
            f"        The behavior of GLogger can be customized by setting the 'GLOGGER_PROVIDER' environment variable.\n"
            f"        This variable determines which log providers are active and available for use. By default, \n"
            f"        'GLOGGER_PROVIDER' is set to 'aws_cloudwatch,local', activating the AWS CloudWatch Logs and\n"
            f"        Local File Logger providers.\n"
            f"\n"
            f"        You can configure this variable to include a comma-separated list of log provider names that you want to \n"
            f"        activate. \n"
            f"        \n"
            f"        For example:\n"
            f"        - To activate AWS CloudWatch Logs only, set {Fore.BLUE}'GLOGGER_PROVIDER' to 'aws_cloudwatch'{Fore.RESET}.\n"
            f"        - To activate both AWS S3 and Azure Blob Storage, set {Fore.BLUE}'GLOGGER_PROVIDER' to 'aws_s3,azure_blob'.\n"
            f"        {Fore.RESET}\n"
            f"\n"
            f"        Use 'glogger providers' to list the available log providers.\n"
            f"\n"
            f"        To run GLogger in watch mode, use the following command:\n"
            f"        glogger <command>\n"
            f"        \n"
            f"        {Fore.MAGENTA}Explanation:{Fore.RESET}\n"
            f"        GLogger's watch mode allows you to monitor the execution of any system command and \n"
            f"        send its logs in real-time to a configured log provider. This feature is useful for\n"
            f"        tracking command output and automatically collecting log records.\n"
            f"\n"
            f"        {Fore.MAGENTA}Here's how it works:{Fore.RESET}\n"
            f"        1. Execute a system command as usual.\n"
            f"        2. GLogger monitors the command's standard output in real-time.\n"
            f"        3. Logs are sent to the configured log provider as the command runs.\n"
            f"        4. You can access and analyze these logs later.\n"
            f"\n"
            f"        {Fore.MAGENTA}To use watch mode, run the following command:{Fore.RESET}\n"
            f"        glogger <command>\n"
            f"\n"
            f"        {Fore.MAGENTA}Example:{Fore.RESET}\n"
            f"        glogger sh my_script.sh\n"
            f"        glogger node my_script.js\n"
            f"\n"
            f"        Please note that the order of the log providers in {Fore.BLUE}'GLOGGER_PROVIDER'{Fore.RESET} \n"
            f"        determines their priority. Active providers will be used in the order they appear in the list.\n"
            f"\n"
            f"        Remember to configure the required environment variables for each log provider you enable \n"
            f"        {Fore.BLUE}'GLOGGER_PROVIDER'{Fore.RESET} to ensure they work correctly.\n"
            f"        "
        )
        print(help_message)

    def version(self):
        print(f"glogger {self.version_tag}")

    def providers(self):
        providers = f"""
        The available log providers are:
        {Fore.MAGENTA}
        - local
        - aws_cloudwatch
        - aws_s3
        - azure_blob
        - azure_insight
        - gcp_logging
        - gcp_storage
        - websocket
        - papertrail
        {Fore.RESET}
        """
        print(providers)

    def environment(self):
        text = (
            f"\n"
            f"        {Fore.MAGENTA}Explanation of Environment Variables:{Fore.RESET}\n"
            f"        - {Fore.GREEN}AWS_ACCESS_KEY_ID:{Fore.RESET} The AWS access key ID for accessing AWS services.\n"
            f"        - {Fore.GREEN}AWS_SECRET_ACCESS_KEY:{Fore.RESET} The AWS secret access key associated with the access key ID.\n"
            f"        - {Fore.GREEN}AWS_REGION:{Fore.RESET} The AWS region where the logs will be stored.\n"
            f"        - {Fore.GREEN}AWS_CLOUDWATCH_LOG_GROUP_NAME:{Fore.RESET} The name of the AWS CloudWatch log group.\n"
            f"        - {Fore.GREEN}AWS_CLOUDWATCH_LOG_STREAM_NAME:{Fore.RESET} The name of the AWS CloudWatch log stream.\n"
            f"        - {Fore.GREEN}AWS_BUCKET_NAME:{Fore.RESET} The name of the AWS S3 bucket where logs will be stored.\n"
            f"        - {Fore.GREEN}AWS_OBJECT_KEY:{Fore.RESET} The key of the AWS S3 object where logs will be stored.\n"
            f"        - {Fore.GREEN}AZURE_STORAGE_CONNECTION_STRING:{Fore.RESET} The connection string for accessing Azure Blob Storage.\n"
            f"        - {Fore.GREEN}AZURE_CONTAINER_NAME:{Fore.RESET} The name of the Azure Blob Storage container.\n"
            f"        - {Fore.GREEN}AZURE_BLOB_NAME:{Fore.RESET} The name of the Azure Blob where logs will be stored.\n"
            f"        - {Fore.GREEN}AZURE_APP_INSIGHTS_INSTRUMENTATION_KEY:{Fore.RESET} The Application Insights instrumentation key for Azure.\n"
            f"        - {Fore.GREEN}GCP_LOG_NAME:{Fore.RESET} The name of the Google Cloud Logging log.\n"
            f"        - {Fore.GREEN}GCP_PROJECT_ID:{Fore.RESET} The ID of the Google Cloud project.\n"
            f"        - {Fore.GREEN}GCP_BUCKET_NAME:{Fore.RESET} The name of the Google Cloud Storage bucket.\n"
            f"        - {Fore.GREEN}GCP_OBJECT_KEY:{Fore.RESET} The key of the Google Cloud Storage object.\n"
            f"        - {Fore.GREEN}WEBSOCKET_URI:{Fore.RESET} The URI for WebSocket communication by {Fore.MAGENTA}GFRANCODEV/GLOGGER SERVER{Fore.RESET}.\n"
            f'        - {Fore.GREEN}LOCAL_FILE_PATH:{Fore.RESET} The local file path where logs will be stored when using the "local" log provider.\n'
            f"        - {Fore.GREEN}PAPERTRAIL_HOST:{Fore.RESET} The hostname or IP address of the Papertrail log destination.\n"
            f"        - {Fore.GREEN}PAPERTRAIL_PORT:{Fore.RESET} The port number for connecting to the Papertrail log destination.                                                               \n"
            f"        "
        )
        print(text)

    def execute(self):
        init(autoreset=True)
        just_fix_windows_console()

        ascii_art = (
            f"\n"
            f"        {Fore.BLUE}\n"
            f"        ▄████  ██▓     ▒█████    ▄████   ▄████ ▓█████  ██▀███  \n"
            f"        ██▒ ▀█▒▓██▒    ▒██▒  ██▒ ██▒ ▀█▒ ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒\n"
            f"        ▒██░▄▄▄░▒██░    ▒██░  ██▒▒██░▄▄▄░▒██░▄▄▄░▒███   ▓██ ░▄█ ▒\n"
            f"        ░▓█  ██▓▒██░    ▒██   ██░░▓█  ██▓░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄  \n"
            f"        ░▒▓███▀▒░██████▒░ ████▓▒░░▒▓███▀▒░▒▓███▀▒░▒████▒░██▓ ▒██▒\n"
            f"        ░▒   ▒ ░ ▒░▓  ░░ ▒░▒░▒░  ░▒   ▒  ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░\n"
            f"        ░   ░ ░ ░ ▒  ░  ░ ▒ ▒░   ░   ░   ░   ░  ░ ░  ░  ░▒ ░ ▒░\n"
            f"        ░ ░   ░   ░ ░   ░ ░ ░ ▒  ░ ░   ░ ░ ░   ░    ░     ░░   ░ \n"
            f"            ░     ░  ░    ░ ░        ░       ░    ░  ░   ░                                                                      \n"
            f"        {Fore.RESET}\n"
            f"        {Fore.CYAN}     {self.version_tag} GFRANCODEV | GLOGGER - Log Aggregator{Fore.RESET}\n"
            f"        "
        )

        print(ascii_art)

        if len(argv) < 2:
            self.help()
            exit(1)

        if str(argv[1]) == "--help" or str(argv[1]) == "-h":
            self.help()
            exit(0)

        if str(argv[1]) == "--providers" or str(argv[1]) == "-p":
            self.providers()
            exit(0)

        if str(argv[1]) == "--env" or str(argv[1]) == "-e":
            self.environment()
            exit(0)

        if str(argv[1]) == "--version" or str(argv[1]) == "-v":
            self.version()
            exit(0)
