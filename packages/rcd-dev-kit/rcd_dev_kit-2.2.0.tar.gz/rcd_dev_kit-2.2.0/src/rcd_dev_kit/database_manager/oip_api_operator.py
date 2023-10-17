import os
import json
import requests


class OipApiOperator:
    """A class for interacting with the Open Innovation Program API."""

    CLIENT_ID = "1ExHsqdpPx3TeinHY1jZQWmD7N5lGJo1"
    CLIENT_SECRET = "XHYRQMtYb1WpUotPZcuRdQSzgFCTwgyUI9YKL1gSooXSqwUePapIL1L6h05Plmzo"

    def __init__(self):
        """Initialize an instance of OipApiOperator."""
        self.auth0_token = None
        self.url = None
        self.payload = None
        self.headers = None
        self.oip_user = os.environ.get("OIP_USERNAME")
        self.oip_password = os.environ.get("OIP_PASSWORD")

    def send_request(self, method: str = "GET") -> dict:
        """
        Send an HTTP request to the specified URL.

        Args:
            method (str, optional): The HTTP request method (e.g., "GET", "POST"). Defaults to "GET".

        Returns:
            dict: A JSON response from the API.

        Raises:
            SyntaxError: If the response status code is not 200 or the response contains error messages.
        """
        response = requests.request(method, self.url, headers=self.headers, data=self.payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()

    def authenticate_auth0(self) -> 'OipApiOperator':
        """
        Authenticate with Auth0 to obtain an access token.

        Returns:
            OipApiOperator: The instance of the class with the Auth0 token set.
        """
        self.payload = json.dumps(
            {
                "connection": "main",
                "grant_type": "password",
                "username": self.oip_user,
                "password": self.oip_password,
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET
            }
        )
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.url = "https://openinnovationprogram.eu.auth0.com/oauth/token"
        json_response = self.send_request(method="POST")

        self.auth0_token = json_response["id_token"]

        return self

    def set_sources(self) -> 'OipApiOperator':
        """
        Set the API endpoint URL for retrieving sources.

        Returns:
            OipApiOperator: The instance of the class with the URL set.
        """
        self.url = "https://openinnovationprogram.api.oip-platform.com/api/v2/sources"
        return self

    def get_all_sources(self) -> dict:
        """
        Get all sources from the API.

        Returns:
            dict: A JSON response containing all sources.

        Raises:
            AssertionError: If the URL endpoint is empty. Run the method .set_sources() first.
        """
        assert self.url, "URL Endpoint is empty. Did you run the method .set_sources()?"
        self.payload = ""
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json',
            'Origin': 'https://openinnovationprogram.com',
            'Authorization': f'Bearer {self.auth0_token}'
        }
        return self.send_request(method="GET")
