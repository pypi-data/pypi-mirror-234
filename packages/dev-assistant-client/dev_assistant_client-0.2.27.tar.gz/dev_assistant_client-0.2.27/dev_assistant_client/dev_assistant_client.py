import asyncio
import argparse
import time

from dotenv import load_dotenv
from colorama import Fore, Style
from dev_assistant_client.client import connect_client
from dev_assistant_client.client_auth import ClientAuth
from dev_assistant_client.utils import APP_URL, read_token

import pkg_resources

load_dotenv()

class DevAssistant:
    
    def __init__(self):
        self.auth = ClientAuth()
        self.package_version = pkg_resources.get_distribution("dev-assistant-client").version
        self.print_header()

    def print_header(self):
        print(Fore.LIGHTGREEN_EX +
            '''
        ╭─────╮   Dev Assistant
        │ ''' + Fore.WHITE + '>_<' + Fore.LIGHTGREEN_EX + ''' │   ''' + Fore.LIGHTYELLOW_EX + 'v' + self.package_version + Fore.LIGHTGREEN_EX + ''' 
        ╰─────╯   ''' + Fore.LIGHTYELLOW_EX + APP_URL + Fore.LIGHTGREEN_EX + '''
        ''' + Style.RESET_ALL)

    def cli(self):
        from dev_assistant_client.cli import cli
        cli()

    def run(self, args=None):
        token = read_token()

        if token is None:
            self.auth.authenticate()
            
        # Parse command line arguments
        parser = argparse.ArgumentParser(prog='dev-assistant-client')
        subparsers = parser.add_subparsers()

        parser_logout = subparsers.add_parser('close')
        parser_logout.set_defaults(func=self.auth.deauthenticate)
                
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(connect_client())
            loop.close()
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting...")        
        finally:
            time.sleep(1)
            
if __name__ == "__main__":
    DevAssistant().run()

