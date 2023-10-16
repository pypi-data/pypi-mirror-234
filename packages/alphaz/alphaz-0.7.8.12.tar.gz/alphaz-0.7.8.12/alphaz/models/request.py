# MODULES
import requests

# ALPHAZ
from alphaz.models.config import AlphaConfig

# CORE
from core import core

LOG = core.get_logger("http")


class AlphaRequest:
    def __init__(self, config: AlphaConfig, log=None):
        """
        Initialize a new AlphaRequest object.

        Args:
            config: The AlphaConfig object to use.
            log: The logger object to use (optional).
        """
        self.config = config
        self.host = self.config.get("host")
        self.log = log

    def get_url(self, route: str) -> str:
        """
        Get the URL for a given route.

        Args:
            route: The route to get the URL for.

        Returns:
            A string representing the URL for the given route.
        """
        if not route.startswith("/"):
            route = "/" + route
        protocol = "https" if self.config.get("ssl") else "http"
        return f"{protocol}://{self.host}{route}"

    def post(self, route: str, data: dict | None = None) -> str | None:
        """
        Send a POST request to the given route.

        Args:
            route: The route to send the POST request to.
            data: The data to include in the POST request (optional).

        Returns:
            The response text from the server, or None if there was an error.
        """
        try:
            response = requests.post(self.get_url(route), data=data, verify=False)
            return response.text
        except requests.exceptions.RequestException as ex:
            if self.log:
                self.log.error(ex)
            return None

    def get(self, route, data={}):
        """
        Makes an HTTP GET request to the given route with the given data.

        Args:
            route (str): The route to make the request to.
            data (dict): The data to include in the request.

        Returns:
            A string representing the response text, or None if an error occurred.
        """
        try:
            response = requests.get(self.get_url(route), params=data, verify=False)
            return str(response.text)
        except Exception as ex:
            if self.log:
                self.log.error(ex)
            return None
