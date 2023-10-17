import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse
from requests import Response
from requests.exceptions import RequestException
import json
import logging

from raga.utils import HTTPClient

class TestHTTPClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://example.com"
        self.http_client = HTTPClient(self.base_url)

    def test_init(self):
        self.assertEqual(self.http_client.base_url, self.base_url)

    def test_validate_base_url_valid(self):
        valid_base_url = "http://example.com"
        validated_base_url = self.http_client.validate_base_url(valid_base_url)
        self.assertEqual(validated_base_url, valid_base_url)

    def test_validate_base_url_invalid(self):
        invalid_base_url = "example.com"
        with self.assertRaises(ValueError):
            self.http_client.validate_base_url(invalid_base_url)

    @patch("raga.utils.http_client.requests.get")
    @patch("raga.utils.http_client.logger.debug")
    def test_get_successful_request(self, mock_logger_debug, mock_requests_get):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "message": "Success message"}

        mock_requests_get.return_value = mock_response

        endpoint = "/api/get"
        params = {"param1": "value1"}
        data = {"key1": "value1"}
        headers = {"Content-Type": "application/json"}

        response = self.http_client.get(endpoint, params=params, data=data, headers=headers)

        mock_requests_get.assert_called_once_with(
            self.base_url + endpoint, params=params, data=json.dumps(data), headers=headers
        )
        
        self.assertEqual(response, {"success": True, "message": "Success message"})



    @patch("raga.utils.http_client.requests.get")
    def test_get_unsuccessful_request(self, mock_requests_get):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {"success": False, "message": "Error message"}

        mock_requests_get.return_value = mock_response

        endpoint = "/api/get"

        with self.assertRaises(ValueError) as cm:
            self.http_client.get(endpoint)

        mock_requests_get.assert_called_once_with(self.base_url + endpoint, params=None, data=None, headers={'Content-Type': 'application/json'})
        self.assertEqual(str(cm.exception), "Request failed with status code 400: Error message")

    @patch("raga.utils.http_client.requests.get")
    def test_get_request_exception(self, mock_requests_get):
        mock_requests_get.side_effect = RequestException()

        endpoint = "/api/get"

        with self.assertRaises(RequestException):
            self.http_client.get(endpoint)

        mock_requests_get.assert_called_once_with(self.base_url + endpoint, params=None, data=None, headers={'Content-Type': 'application/json'})

    @patch("raga.utils.http_client.requests.request")
    @patch("raga.utils.http_client.logger.debug")
    def test_post_successful_request(self, mock_logger_debug, mock_requests_request):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 201
        mock_response.json.return_value = {"success": True, "message": "Success message"}

        mock_requests_request.return_value = mock_response

        endpoint = "/api/post"
        data = {"key1": "value1"}
        headers = {"Content-Type": "application/json"}

        response = self.http_client.post(endpoint, data=data, headers=headers)

        mock_requests_request.assert_called_once_with(
            "POST", self.base_url + endpoint, json=data, headers=headers
        )

        self.assertEqual(response, {"success": True, "message": "Success message"})

        
    @patch("raga.utils.http_client.requests.request")
    def test_post_unsuccessful_request(self, mock_requests_request):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {"success": False, "message": "Error message"}

        mock_requests_request.return_value = mock_response

        endpoint = "/api/post"

        with self.assertRaises(ValueError) as cm:
            self.http_client.post(endpoint)

        mock_requests_request.assert_called_once_with(
            "POST", self.base_url + endpoint, json=None, headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(str(cm.exception), "Request failed with status code 400: Error message")

    @patch("raga.utils.http_client.requests.request")
    def test_post_request_exception(self, mock_requests_request):
        mock_requests_request.side_effect = RequestException()

        endpoint = "/api/post"

        with self.assertRaises(RequestException):
            self.http_client.post(endpoint)

        mock_requests_request.assert_called_once_with(
            "POST", self.base_url + endpoint, json=None, headers={'Content-Type': 'application/json'}
        )

if __name__ == "__main__":
    unittest.main()
