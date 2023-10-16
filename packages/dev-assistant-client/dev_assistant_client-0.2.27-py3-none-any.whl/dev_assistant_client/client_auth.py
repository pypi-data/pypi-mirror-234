import os
from colorama import Fore, Style
from dev_assistant_client.config import api_client
from dev_assistant_client.utils import save_token, delete_token, get_client_id, APP_URL
import webbrowser

class ClientAuth:
    """
    The ClientAuth class handles client-based authentication operations.
    This includes generating a token for the client after authenticating via a web browser.
    """
    
    def authenticate(self):
        """
        Opens the authentication page in the browser for the client to be authenticated.
        Once authenticated, the user should be provided with a token that they'll enter here.
        """
        print("\nOpening authentication page in browser...")
        
        # Determine the URL based on environment
        base_url = APP_URL
        
        # current client id
        client_id = get_client_id()
        
        webbrowser.open(f'{base_url}/auth/{client_id}?client_type=cli')
        token = input("Enter the token received after successful authentication: ")
        
        if token:
            save_token(token)
            print(Fore.LIGHTGREEN_EX + "Authenticated successfully!" + Style.RESET_ALL)
            return True
        else:
            print(Fore.LIGHTRED_EX + "Authentication failed. Please try again." + Style.RESET_ALL)
            return False

    def deauthenticate(self):
        """
        Deauthenticates the client by deleting the locally stored token.
        """
        try:
            delete_token()
            print("Successfully deauthenticated.")
        except FileNotFoundError:
            print("Client is not currently authenticated.")
