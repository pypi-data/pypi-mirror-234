import json
import logging
import requests
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

class HTTPClient:
    def __init__(self, base_url: str):
        self.base_url = self.validate_base_url(base_url)
        logger.debug(f"Base URL: {self.base_url}")

    def remove_extra_slashes(self, url):
        parsed_url = urlparse(url)
        cleaned_path = "/".join(segment for segment in parsed_url.path.split("/") if segment)
        cleaned_url = urlunparse(parsed_url._replace(path=cleaned_path))
        return cleaned_url

    def validate_base_url(self, base_url: str) -> str:
        """
        Validates the base URL format and returns the validated URL.

        Args:
            base_url (str): The base URL to validate.

        Returns:
            str: The validated base URL.

        Raises:
            ValueError: If the base URL format is invalid.
        """
        base_url = f"{base_url}/"
        parsed_url = urlparse(base_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid base URL. Must be in the format 'http(s)://domain.com'.")
        return base_url

    def get(self, endpoint: str, params=None, data=None, headers=None):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the GET request to.
            params (dict, optional): The query parameters for the GET request. Defaults to None.
            data (dict, optional): The request payload for the GET request. Defaults to None.
            headers (dict, optional): The headers for the GET request. Defaults to None.

        Returns:
            dict: The JSON response from the GET request.

        Raises:
            ValueError: If the GET request is unsuccessful or returns an error response.
        """
        url = self.remove_extra_slashes(self.base_url + endpoint)
        logger.debug(f"API ENDPOINT {url}")
        logger.debug(f"API PARAMS {json.dumps(params)}")
        logger.debug(f"API DATA {json.dumps(data)}")
        logger.debug(f"API HEADER {json.dumps(headers)}")

        default_headers = {'Content-Type': 'application/json'}
        if headers:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers
            
        if data:
            data = json.dumps(data)

        response = requests.get(url, params=params, data=data, headers=headers)
        logger.debug(f"API RESPONSE {response.json()}")
        status_code = response.status_code
        json_data = response.json()

        if status_code in (200, 201) and json_data.get("success"):
            print(json_data.get("message"))
            logger.debug(json_data.get("message"))
            return json_data
        else:
            error_message = json_data.get("message")
            if error_message:
                raise ValueError(f"Request failed with status code {status_code}: {error_message}")
            else:
                raise ValueError(f"Request failed with status code {status_code}")

    def post(self, endpoint: str, data=None, headers=None):
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the POST request to.
            data (dict, optional): The request payload for the POST request. Defaults to None.
            headers (dict, optional): The headers for the POST request. Defaults to None.

        Returns:
            dict: The JSON response from the POST request.

        Raises:
            ValueError: If the POST request is unsuccessful or returns an error response.
        """
        url = self.remove_extra_slashes(self.base_url + endpoint)
        logger.debug(f"API ENDPOINT {endpoint}")
        logger.debug(f"API DATA {json.dumps(data)}")
        logger.debug(f"API HEADER {json.dumps(headers)}")

        default_headers = {'Content-Type': 'application/json'}
        if headers:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers

        response = requests.request('POST', url, json=data, headers=headers)
        logger.debug(f"API RESPONSE {response.json()}")
        status_code = response.status_code
        json_data = response.json()

        if status_code in (200, 201) and json_data.get("success"):
            print(json_data.get("message"))
            logger.debug(json_data.get("message"))
            return json_data
        else:
            error_message = json_data.get("message")
            if error_message:
                raise ValueError(f"Request failed with status code {status_code}: {error_message}")
            else:
                raise ValueError(f"Request failed with status code {status_code}")


