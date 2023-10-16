import unittest
from unittest.mock import MagicMock, patch
from unittest import mock
import pandas as pd
from raga import *
from raga.utils import on_upload_success, on_upload_failed
from raga.dataset import Dataset
class TestDataset(unittest.TestCase):

    def setUp(self):
        self.test_session = TestSession("project_name", "run_name", u_test=True)
        self.test_session.project_id = "project_id"
        self.test_session.token = "token"
        self.dataset_name = "my_dataset"
        self.test_session.experiment_id = "experiment_id"
        self.dataset_creds = None
        self.dataset = Dataset(self.test_session, self.dataset_name, self.dataset_creds, u_test=True)
        self.dataset.dataset_id = "12345"
        self.dataset.zip_file = "experiment_experiment_id.zip"

    def test_create_dataset(self):
        expected_dataset_id = "12345"
        mock_create_dataset = MagicMock(return_value={"data": {"id": expected_dataset_id}})
        self.test_session.http_client.post = mock_create_dataset

        dataset_id = self.dataset.create_dataset()

        self.assertEqual(dataset_id, expected_dataset_id)
        mock_create_dataset.assert_called_once_with(
            "api/dataset",
            {"name": self.dataset_name, "projectId": self.test_session.project_id, "experimentId":self.test_session.experiment_id},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )


    def test_get_pre_signed_s3_url(self):
        expected_signed_upload_path = "https://s3.amazonaws.com/my-bucket/upload"
        expected_file_path = "my-bucket/folder/file.zip"
        mock_get_pre_signed_url = MagicMock(return_value={"data": {"signedUploadPath": expected_signed_upload_path, "filePath": expected_file_path}})
        self.test_session.http_client.get = mock_get_pre_signed_url

        signed_upload_path, file_path = self.dataset.get_pre_signed_s3_url("file.zip")

        self.assertEqual(signed_upload_path, expected_signed_upload_path)
        self.assertEqual(file_path, expected_file_path)
        mock_get_pre_signed_url.assert_called_once_with(
            "api/dataset/uploadpath",
            None,
            {"experimentId": self.test_session.experiment_id, "fileName": "file.zip", "contentType":"application/zip"},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

    def test_create_dataset_load_definition(self):
        self.dataset.dataset_id = "dataset_id"
        file_path = "file_path"
        data_type = "pandas"
        arguments = {"arg1": "value1", "arg2": "value2"}
        mock_post = MagicMock(return_value={"data": {"id":"id"}})
        self.test_session.http_client.post = mock_post

        result = self.dataset.create_dataset_load_definition(file_path, data_type, arguments)

        mock_post.assert_called_once_with(
            "api/dataset/definition",
            {
                "datasetId": "dataset_id",
                "filePath": "file_path",
                "type": "pandas",
                "arguments": {"arg1": "value1", "arg2": "value2"},
            },
            {"Authorization": "Bearer token"},
        )
        self.assertEqual(result, "id")


    @mock.patch("raga.dataset.create_csv_and_zip_from_data_frame")
    @mock.patch("raga.dataset.upload_file")
    @mock.patch("raga.dataset.delete_files")
    @mock.patch("raga.dataset.Dataset.create_dataset_load_definition")
    @mock.patch("raga.dataset.Dataset.notify_server")
    @mock.patch("raga.dataset.Dataset.get_pre_signed_s3_url")
    def test_load_data_frame(self, mock_get_pre_signed_s3_url, mock_notify_server,
                             mock_create_dataset_load_definition, mock_delete_files,
                             mock_upload_file, mock_create_csv_and_zip_from_data_frame):
        data_frame = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        dataset_column = [{"name": "col1", "model": "", "type": "prediction", "description": ""}]
        csv_file = "experiment_experiment_id.csv"
        zip_file = "experiment_experiment_id.zip"
        signed_upload_path = "https://example.com/upload"
        file_path = "path/to/zip_file"

        mock_get_pre_signed_s3_url.return_value = signed_upload_path, file_path
        mock_create_csv_and_zip_from_data_frame.return_value = None
        mock_upload_file.return_value = None
        mock_delete_files.return_value = None
        mock_create_dataset_load_definition.return_value = None
        mock_notify_server.return_value = None

        self.dataset.load_data_frame(data_frame, dataset_column)

        mock_create_csv_and_zip_from_data_frame.assert_called_once_with(data_frame, csv_file, zip_file)
        mock_get_pre_signed_s3_url.assert_called_once_with(zip_file)
        mock_upload_file.assert_called_once_with(signed_upload_path, zip_file, success_callback=on_upload_success,
                                                 failure_callback=on_upload_failed)
        mock_delete_files.assert_called_once_with(csv_file, zip_file)
        mock_create_dataset_load_definition.assert_called_once_with( file_path, "csv", dataset_column)
        mock_notify_server.assert_called_once()

    @mock.patch("raga.dataset.Dataset.get_pre_signed_s3_url")
    @mock.patch("raga.dataset.upload_file")
    @mock.patch("raga.dataset.delete_files")
    def test_load_data_frame_upload_failure(
        self,
        mock_delete_files,
        mock_upload_file,
        mock_get_pre_signed_s3_url,
    ):
        data_frame = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        dataset_column = "dataset_column"

        mock_get_pre_signed_s3_url.return_value = ("signed_upload_path", "file_path")
        mock_upload_file.side_effect = Exception("Upload failed")
        mock_delete_files.return_value = None

        with self.assertRaises(Exception) as context:
            self.dataset.load_data_frame(data_frame, dataset_column)
            self.assertEqual(context.exception, "Upload failed")

            mock_get_pre_signed_s3_url.assert_called_once_with(self.dataset.zip_file)
            mock_upload_file.assert_called_once_with(
                "signed_upload_path",
                self.dataset.zip_file,
                success_callback=on_upload_success,
                failure_callback=on_upload_failed,
            )
            mock_delete_files.assert_called_once_with(
                self.dataset.csv_file, self.dataset.zip_file
            )



    @mock.patch('time.sleep')
    @mock.patch('builtins.print')
    def test_load_success(self, mock_print, mock_sleep):
        # Mock the necessary methods
        mock_initialize = MagicMock()
        self.dataset.initialize = mock_initialize

        # Call the method
        self.dataset.load(data='data', schema='schema', format='format', model_name='model_name',
                          inference_col_name='inference_col', embedding_col_name='embedding_col')

        # Assert the expected calls and prints
        mock_initialize.assert_called_once_with('data', 'schema', 'format', 'model_name',
                                                'inference_col', 'embedding_col')
        mock_print.assert_called_once_with("Data loaded successful!")
        mock_sleep.assert_not_called()

    @mock.patch('time.sleep')
    def test_load_network_error(self, mock_sleep):
       mock_initialize = MagicMock(side_effect=requests.exceptions.RequestException("Network error"))

       with mock.patch('raga.dataset.Dataset.initialize', side_effect=mock_initialize), \
                mock.patch('builtins.print') as mock_print:
            # Set the MAX_RETRIES to 3 for testing
            self.dataset.MAX_RETRIES = 3
            self.dataset.RETRY_DELAY = 1
            # Call the method
            self.dataset.load(data='data', schema='schema', format='format', model_name='model_name',
                          inference_col_name='inference_col', embedding_col_name='embedding_col')
            
            # Assert the expected prints and retries
            expected_calls = [
                mock.call('Network error occurred: Network error'),
                mock.call('Retrying in 1 second(s)...'),
                mock.call('Network error occurred: Network error'),
                mock.call('Retrying in 1 second(s)...'),
                mock.call('Network error occurred: Network error')
            ]
            mock_print.assert_has_calls(expected_calls)
            self.assertEqual(mock_initialize.call_count, 3)
            mock_sleep.assert_called_with(1)

    def test_load_key_error(self):
       mock_initialize = MagicMock(side_effect=KeyError("Key error"))

       with mock.patch('raga.dataset.Dataset.initialize', side_effect=mock_initialize), \
                mock.patch('builtins.print') as mock_print, \
                    self.assertRaises(SystemExit) as cm:
           
            # Call the method
            self.dataset.load(data='data', schema='schema', format='format', model_name='model_name',
                          inference_col_name='inference_col', embedding_col_name='embedding_col')
            
            # Assert the expected prints and retries
            mock_initialize.assert_called_once()
            mock_print.assert_called_with('Key error occurred: Key error')
            self.assertEqual(cm.exception.code, 1)
            
    def test_load_value_error(self):
        mock_initialize = MagicMock(side_effect=ValueError("Value error"))

        with mock.patch('raga.dataset.Dataset.initialize', side_effect=mock_initialize), \
                mock.patch('builtins.print') as mock_print, \
                    self.assertRaises(SystemExit) as cm:
           
            # Call the method
            self.dataset.load(data='data', schema='schema', format='format', model_name='model_name',
                          inference_col_name='inference_col', embedding_col_name='embedding_col')
            
            # Assert the expected prints and retries
            mock_initialize.assert_called_once()
            mock_print.assert_called_with('Value error occurred: Value error')
            self.assertEqual(cm.exception.code, 1)

    def test_load_unexpected_error(self):
        mock_initialize = MagicMock(side_effect=Exception("Unexpected error"))

        with mock.patch('raga.dataset.Dataset.initialize', side_effect=mock_initialize), \
                mock.patch('builtins.print') as mock_print, \
                    self.assertRaises(SystemExit) as cm:
           
            # Call the method
            self.dataset.load(data='data', schema='schema', format='format', model_name='model_name',
                          inference_col_name='inference_col', embedding_col_name='embedding_col')
            
            # Assert the expected prints and retries
            mock_initialize.assert_called_once()
            mock_print.assert_called_with('An unexpected error occurred: Unexpected error')
            self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
