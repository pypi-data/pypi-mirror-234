import os
import requests
import json
from urllib.parse import urlparse

class APIClient:
    def __init__(self, base_url, cert_file=None, key_file=None, token=None):
        parsed_url = urlparse(base_url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.cert_file = cert_file
        self.key_file = key_file
        self.token = token
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "User-Agent": "DevAssistantCLI/0.0.2",
            "Authorization": f"Bearer {self.token}" if self.token else None
        }
        app_env = os.environ.get("APP_ENV")
        self.verify = False if app_env and app_env.lower() == "development" else True
    
    def _make_request(self, method, endpoint, data=None):
        
        # if endpoint starts with https:// or http://, use that as the base url
        if endpoint.startswith("https://") or endpoint.startswith("http://"):
            self.base_url = endpoint
            endpoint = ""
               
        url = self.base_url + endpoint
        payload = json.dumps(data) if data else None
        
        cert = (self.cert_file, self.key_file) if self.cert_file and self.key_file else None
        response = requests.request(method, url, data=payload, headers=self.headers, cert=cert, verify=self.verify)
        
        return response        
            
    def get(self, endpoint):
        return self._make_request("GET", endpoint)
    
    def post(self, endpoint, data=None):
        return self._make_request("POST", endpoint, data)
    
    def put(self, endpoint, data=None):
        return self._make_request("PUT", endpoint, data)
    
    def delete(self, endpoint):
        return self._make_request("DELETE", endpoint)
