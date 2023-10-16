import argparse
import os
from colorama import Fore, Style
from dotenv import load_dotenv
import requests
from packaging import version
import pkg_resources

from dev_assistant_client.dev_assistant_client import DevAssistant

load_dotenv()


def check_for_update():
    """
    Checks if there's an update available for the 'dev-assistant-client' package.
    Compares the current version with the latest version available on PyPI.
    Returns:
        bool: True if an update is available, False otherwise.
    """
    
    response = requests.get(f"https://pypi.org/pypi/dev-assistant-client/json")
    latest_version = response.json()["info"]["version"]

    current_version = pkg_resources.get_distribution("dev-assistant-client").version

    return version.parse(latest_version) > version.parse(current_version)


def cli():
    """
    The main CLI entry point. Handles the command-line arguments, checks for updates,
    and runs the DevAssistant client.
    """
    
    try:
        if check_for_update():
            print(Fore.LIGHTYELLOW_EX + "📦 New version available! "  + Style.RESET_ALL + "\nPlease run 'pip install --upgrade dev-assistant-client' to upgrade." )
    except:
        # Fine if this fails
        DevAssistant().run()

    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # Setup CLI
    parser = argparse.ArgumentParser(description="Dev Assistant CLI.")
    parser.add_argument(
        "-d", "--debug", action="store_true", default=DEBUG, help="prints extra information"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show program's version number and exit"
    )
    parser.add_argument(
        "-x", "--close", action="store_true", help="close the connection with the server"
    )
    
    args = parser.parse_args()

    if args.version:
        print("Dev Assistant", pkg_resources.get_distribution("dev-assistant-client").version)
        return

    DevAssistant().run()