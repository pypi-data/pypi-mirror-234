import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, Mock, call
from requests import Response
import requests
from raga import TestSession

class TestTestSession(unittest.TestCase):

    def setUp(self):
        self.project_name = "project_name"
        self.run_name = "run_name"
        self.mock_http_client = MagicMock()
        self.test_session = TestSession(self.project_name, self.run_name, u_test=True)
        self.test_session.http_client = self.mock_http_client

    def test_create_token(self):
        expected_token = "token"
        mock_response_data = {"data": {"token": expected_token}}
        self.mock_http_client.post.return_value = mock_response_data

        # Call the method
        token = self.test_session.create_token()

        # Assert the expected token is returned
        self.assertEqual(token, expected_token)

    def test_create_token_missing_token(self):
        mock_response_data = {"data": {}}
        self.mock_http_client.post.return_value = mock_response_data

        # Call the method and assert it raises a KeyError
        with self.assertRaises(KeyError):
            self.test_session.create_token()

    def test_get_project_id(self):
        expected_project_id = "project_id"
        mock_response_data = {"data": {"id": expected_project_id}}
        self.mock_http_client.get.return_value = mock_response_data

        # Call the method
        project_id = self.test_session.get_project_id()

        # Assert the expected project ID is returned
        self.assertEqual(project_id, expected_project_id)

    def test_get_project_id_missing_project_id(self):
        mock_response_data = {"data": {}}
        self.mock_http_client.get.return_value = mock_response_data

        # Call the method and assert it raises a KeyError
        with self.assertRaises(KeyError):
            self.test_session.get_project_id()

    def test_create_experiment(self):
        expected_experiment_id = "experiment_id"
        mock_response_data = {"data": {"id": expected_experiment_id}}
        self.mock_http_client.post.return_value = mock_response_data

        # Call the method
        experiment_id = self.test_session.create_experiment()

        # Assert the expected experiment ID is returned
        self.assertEqual(experiment_id, expected_experiment_id)

    def test_create_experiment_missing_experiment_id(self):
        mock_response_data = {"data": {}}
        self.mock_http_client.post.return_value = mock_response_data

        # Call the method and assert it raises a KeyError
        with self.assertRaises(KeyError):
            self.test_session.create_experiment()

    @patch("raga.test_session.HTTPClient")
    def test_get_project_id(self, mock_http_client):
        # Create a TestSession instance
        test_session = TestSession("project_name", "run_name", u_test=True)

        # Mock the HTTPClient instance and its get method
        mock_get = Mock(return_value={"data": {"id": "project_id"}})
        mock_http_client.return_value.get = mock_get

        # Call the get_project_id method
        project_id = test_session.get_project_id()

        # Verify the expected method calls on the mock HTTPClient
        mock_http_client.assert_called_once()
        mock_get.assert_called_once_with(
            "api/project",
            params={"name": "project_name"},
            headers={"Authorization": f'Bearer {test_session.token}'},
        )

        # Verify the returned project_id
        self.assertEqual(project_id, "project_id")

    @patch("raga.test_session.HTTPClient")
    def test_get_project_id_no_data(self, mock_http_client):
        # Create a TestSession instance
        test_session = TestSession("project_name", "run_name", u_test=True)
        # Mock the HTTPClient instance and its get method
        mock_get = Mock(return_value={})
        mock_http_client.return_value.get = mock_get

        with self.assertRaises(KeyError):
            test_session.get_project_id()

        mock_http_client.assert_called_once()
        mock_get.assert_called_once_with(
            "api/project",
            params={"name": "project_name"},
            headers={"Authorization": f'Bearer {self.test_session.token}'},
        )

    @patch("raga.test_session.HTTPClient")
    def test_get_project_id_invalid_response(self, mock_http_client):
        # Create a TestSession instance
        test_session = TestSession("project_name", "run_name", u_test=True)
        # Mock the HTTPClient instance and its get method
        mock_get = Mock(return_value="invalid_response")
        mock_http_client.return_value.get = mock_get

        with self.assertRaises(ValueError):
            test_session.get_project_id()

        mock_http_client.assert_called_once()
        mock_get.assert_called_once_with(
            "api/project",
            params={"name": "project_name"},
            headers={"Authorization": f'Bearer {self.test_session.token}'},
        )

    @patch("raga.test_session.HTTPClient")
    def test_create_experiment(self, mock_http_client):
        # Create a TestSession instance
        test_session = TestSession("project_name", "run_name", u_test=True)
        # Mock the HTTPClient instance and its post method
        mock_post = Mock(return_value={"data": {"id": "experiment_id"}})
        mock_http_client.return_value.post = mock_post

        experiment_id = test_session.create_experiment()

        mock_http_client.assert_called_once()
        mock_post.assert_called_once_with(
            "api/experiment",
            {"name": "run_name", "projectId": self.test_session.project_id},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )
        self.assertEqual(experiment_id, "experiment_id")

    @patch("raga.test_session.HTTPClient")
    def test_create_experiment_no_data(self, mock_http_client):
        # Create a TestSession instance
        test_session = TestSession("project_name", "run_name", u_test=True)
        # Mock the HTTPClient instance and its post method
        mock_post = Mock(return_value={})
        mock_http_client.return_value.post = mock_post

        with self.assertRaises(KeyError):
            test_session.create_experiment()

        mock_http_client.assert_called_once()
        mock_post.assert_called_once_with(
            "api/experiment",
            {"name": "run_name", "projectId": self.test_session.project_id},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

    @patch("raga.test_session.HTTPClient")
    def test_create_experiment_invalid_response(self, mock_http_client):
        # Create a TestSession instance
        test_session = TestSession("project_name", "run_name", u_test=True)
        # Mock the HTTPClient instance and its post method
        mock_post = Mock(return_value="invalid_response")
        mock_http_client.return_value.post = mock_post

        with self.assertRaises(ValueError):
            test_session.create_experiment()

        mock_http_client.assert_called_once()
        mock_post.assert_called_once_with(
            "api/experiment",
            {"name": "run_name", "projectId": self.test_session.project_id},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )
    
    def test_initialize_successful(self):
        mock_create_token = MagicMock(return_value="token")
        mock_get_project_id = MagicMock(return_value="project_id")
        mock_create_experiment = MagicMock(return_value="experiment_id")

        self.test_session.create_token = mock_create_token
        self.test_session.get_project_id = mock_get_project_id
        self.test_session.create_experiment = mock_create_experiment

        # Call the method
        self.test_session.initialize()

        # Assert the expected values are set
        self.assertEqual(self.test_session.token, "token")
        self.assertEqual(self.test_session.project_id, "project_id")
        self.assertEqual(self.test_session.experiment_id, "experiment_id")
        mock_create_token.assert_called_once()
        mock_get_project_id.assert_called_once()
        mock_create_experiment.assert_called_once()

    def test_initialize_network_error(self):
        mock_create_token = MagicMock(side_effect=requests.exceptions.RequestException("Network error"))
        mock_get_project_id = MagicMock()
        mock_create_experiment = MagicMock()

        self.test_session.create_token = mock_create_token
        self.test_session.get_project_id = mock_get_project_id
        self.test_session.create_experiment = mock_create_experiment

        # Call the method
        with patch('builtins.print') as mock_print:
            # Set the MAX_RETRIES to 3 for testing
            self.test_session.MAX_RETRIES = 3
            self.test_session.initialize()

            # Assert the expected prints and retries
            expected_calls = [
                call('Network error occurred: Network error'),
                call(f'Retrying in {self.test_session.RETRY_DELAY} second(s)...'),
                call('Network error occurred: Network error'),
                call(f'Retrying in {self.test_session.RETRY_DELAY} second(s)...'),
                call('Network error occurred: Network error')
            ]
            mock_print.assert_has_calls(expected_calls)
            self.assertEqual(mock_print.call_count, len(expected_calls))
            self.assertEqual(mock_create_token.call_count, self.test_session.MAX_RETRIES)
            self.assertEqual(mock_get_project_id.call_count, 0)
            self.assertEqual(mock_create_experiment.call_count, 0)

    def test_initialize_key_error(self):
        mock_create_token = MagicMock(return_value="token")
        mock_get_project_id = MagicMock(side_effect=KeyError("Invalid response data"))
        mock_create_experiment = MagicMock()

        self.test_session.create_token = mock_create_token
        self.test_session.get_project_id = mock_get_project_id
        self.test_session.create_experiment = mock_create_experiment
       
        # Call the method
        with patch('builtins.print') as mock_print, \
            self.assertRaises(SystemExit) as cm:
            self.test_session.initialize()

            # Assert the expected prints and no retries
            expected_calls = [
                call("Key error occurred: 'Invalid response data'")
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(mock_print.call_count, 1)
            self.assertEqual(mock_create_token.call_count, 1)
            self.assertEqual(mock_get_project_id.call_count, 1)
            self.assertEqual(mock_create_experiment.call_count, 0)
            self.assertEqual(cm.exception.code, 1)
            
    
    def test_initialize_value_error(self):
        mock_create_token = MagicMock(return_value="token")
        mock_get_project_id = MagicMock(side_effect=ValueError("Invalid response data. Expected a dictionary."))
        mock_create_experiment = MagicMock()

        self.test_session.create_token = mock_create_token
        self.test_session.get_project_id = mock_get_project_id
        self.test_session.create_experiment = mock_create_experiment

        # Call the method
        with patch('builtins.print') as mock_print, \
            self.assertRaises(SystemExit) as cm:
            self.test_session.initialize()

            # Assert the expected prints and no retries
            expected_calls = [
                call('Value error occurred: Invalid response data. Expected a dictionary.')
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(mock_print.call_count, 1)
            self.assertEqual(mock_create_token.call_count, 1)
            self.assertEqual(mock_get_project_id.call_count, 1)
            self.assertEqual(mock_create_experiment.call_count, 0)
            self.assertEqual(cm.exception.code, 1)


    def test_initialize_unexpected_error(self):
        mock_create_token = MagicMock(return_value="token")
        mock_get_project_id = MagicMock(return_value="project_id")
        mock_create_experiment = MagicMock(side_effect=Exception("An unexpected error occurred"))

        self.test_session.create_token = mock_create_token
        self.test_session.get_project_id = mock_get_project_id
        self.test_session.create_experiment = mock_create_experiment
    
        # Call the method
        with patch('builtins.print') as mock_print, \
             self.assertRaises(SystemExit) as cm:
            self.test_session.initialize()

            # Assert the expected prints and no retries
            expected_calls = [
                call("An unexpected error occurred: An unexpected error occurred")
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(mock_print.call_count, 1)
            self.assertEqual(mock_create_token.call_count, 1)
            self.assertEqual(mock_get_project_id.call_count, 1)
            self.assertEqual(mock_create_experiment.call_count, 1)
            self.assertEqual(cm.exception.code, 1)

    def test_run_successful(self):
        payload = {"key": "value"}

        # Call the method
        self.test_session.add(payload)

        self.assertEqual(len(self.test_session.test_list), 1)
        self.assertTrue(self.test_session.added)
    
    def test_add_empty_payload(self):
        with self.assertRaises(ValueError) as cm:
            self.test_session.add({})
        self.assertEqual(str(cm.exception), "model_comparison_check_payload must be a non-empty dictionary.")
        self.assertEqual(len(self.test_session.test_list), 0)
        self.assertFalse(self.test_session.added)

    def test_run_success(self):
        self.test_session.added = True
        self.test_session.test_list = [{"key": "value"}]
        self.test_session.token = "test_token"
        
        mock_post = MagicMock(return_value={"data": "test_result"})
        with patch.object(self.test_session.http_client, 'post', mock_post):
            self.test_session.run()

        mock_post.assert_called_once_with("api/experiment/test", data={"key": "value"}, headers={"Authorization": "Bearer test_token"})

    def test_run_not_added(self):
        with self.assertRaises(ValueError) as cm:
            self.test_session.run()

        self.assertEqual(str(cm.exception), "add() is not called. Call add() before run().")

    def test_run_empty_list(self):
        self.test_session.added = True

        with self.assertRaises(ValueError) as cm:
            self.test_session.run()

        self.assertEqual(str(cm.exception), "Test not found.")

    def test_run_network_error_retry(self):
        self.test_session.added = True
        self.test_session.token = "test_token"
        self.test_session.test_list = [{"key": "value"}]
        
        mock_post = MagicMock(side_effect=requests.exceptions.RequestException())
        with patch.object(self.test_session.http_client, 'post', mock_post):
            with patch('time.sleep') as mock_sleep:
                 self.test_session.run()

        mock_post.assert_called_with("api/experiment/test", data={"key": "value"}, headers={"Authorization": "Bearer test_token"})
        self.assertEqual(mock_sleep.call_count, 2)  # Verify that it retried 3 times

    def test_run_key_error_no_retry(self):
        self.test_session.added = True
        self.test_session.test_list = [{"key": "value"}]
        
        mock_post = MagicMock(side_effect=KeyError("Invalid key"))
        with patch.object(self.test_session.http_client, 'post', mock_post), \
            mock.patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                self.test_session.run()

            mock_print.assert_called_with("Key error occurred: 'Invalid key'")

    def test_run_value_error_no_retry(self):
        self.test_session.added = True
        self.test_session.test_list = [{"key": "value"}]
        
        mock_post = MagicMock(side_effect=ValueError("Invalid value"))
        with patch.object(self.test_session.http_client, 'post', mock_post):
            with self.assertRaises(SystemExit) as cm, \
                mock.patch('builtins.print') as mock_print:
                self.test_session.run()

        mock_print.assert_called_with("Value error occurred: Invalid value")

    def test_run_unexpected_error_no_retry(self):
        self.test_session.added = True
        self.test_session.test_list = [{"key": "value"}]
        
        mock_post = MagicMock(side_effect=Exception("Unexpected error"))
        with patch.object(self.test_session.http_client, 'post', mock_post):
            with self.assertRaises(SystemExit) as cm, \
                mock.patch('builtins.print') as mock_print:
                self.test_session.run()

        mock_print.assert_called_with("An unexpected error occurred: Unexpected error")

if __name__ == '__main__':
    unittest.main()
