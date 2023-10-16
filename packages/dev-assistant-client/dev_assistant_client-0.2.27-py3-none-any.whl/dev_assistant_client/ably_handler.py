import asyncio
import json
import requests
from ably import AblyRealtime
from colorama import Fore, Style
from dev_assistant_client.config import api_client
from dev_assistant_client.io import IOAssistant
from dev_assistant_client.utils import CLIENT_ID, dd, now, read_token

class AblyHandler:
    def init_ably(self):
        try:
            api_client.token = read_token()
            api_client.headers["Authorization"] = f"Bearer {api_client.token}"
            response = api_client.get(f"/auth/{CLIENT_ID}/ably")
            token_request = json.loads(response.content)

            token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
            response = requests.post(token_url, json=token_request)
            token = response.json()["token"]
            realtime = AblyRealtime(token=token)
        except Exception as e:
            dd(e)
            return None

        return realtime

    async def ably_connect(self):
        print(now(), "WebSockets...\t", sep="\t", end="\t")
        realtime = self.init_ably()
        if realtime is None:
            print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL)
            return
        
        print(Fore.LIGHTGREEN_EX + "Connected!" + Style.RESET_ALL)

        
        print(now(), "Private channel...", sep="\t", end="\t")
        privateChannel = realtime.channels.get(f"private:dev-assistant-{CLIENT_ID}")
        if privateChannel is None:
            print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL)
            return
        
        print(Fore.LIGHTGREEN_EX + "Connected!" + Style.RESET_ALL)

        await privateChannel.subscribe(self.ably_message)
        print(now(), "Ready!", "Listening for instructions...", sep="\t")
              
        while True:
            await asyncio.sleep(1)
        
    def ably_message(self, message):
        IOAssistant.process_message(message)