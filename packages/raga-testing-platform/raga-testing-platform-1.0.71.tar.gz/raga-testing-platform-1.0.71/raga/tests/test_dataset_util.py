import os
import unittest
from unittest import mock
import pandas as pd
from raga import upload_file, create_csv_and_zip_from_data_frame, delete_files, StringElement, data_frame_extractor
from raga.utils.dataset_util import FileUploadError

class TestFileUpload(unittest.TestCase):
    
    @mock.patch("raga.logger.debug")
    @mock.patch("os.remove")
    @mock.patch("os.path.exists")
    def test_delete_files_success(self, mock_path_exists, mock_remove, mock_logger_debug):
        mock_path_exists.side_effect = [True, True]
        mock_remove.return_value = None

        csv_file = "test.csv"
        zip_file = "test.zip"

        result = delete_files(csv_file, zip_file)

        mock_path_exists.assert_any_call(csv_file)
        mock_remove.assert_any_call(csv_file)
        mock_path_exists.assert_any_call(zip_file)
        mock_remove.assert_any_call(zip_file)
        self.assertTrue(result)

    @mock.patch("raga.logger.debug")
    @mock.patch("os.path.exists")
    def test_delete_files_csv_file_not_found(self, mock_path_exists, mock_logger_debug):
        mock_path_exists.return_value = False

        csv_file = "test.csv"
        zip_file = "test.zip"

        with self.assertRaises(FileNotFoundError) as context:
            delete_files(csv_file, zip_file)

        mock_path_exists.assert_called_with(csv_file)
        self.assertEqual(str(context.exception), "CSV file not found.")

    @mock.patch("raga.logger.debug")
    @mock.patch("os.remove")
    @mock.patch("os.path.exists")
    def test_delete_files_zip_file_not_found(self, mock_path_exists, mock_remove, mock_logger_debug):
        mock_path_exists.side_effect = [True, False]
        mock_remove.return_value = None

        csv_file = "test.csv"
        zip_file = "test.zip"

        with self.assertRaises(FileNotFoundError) as context:
            delete_files(csv_file, zip_file)

        mock_path_exists.assert_any_call(csv_file)
        mock_remove.assert_any_call(csv_file)
        mock_path_exists.assert_any_call(zip_file)
        self.assertEqual(str(context.exception), "Zip file not found.")


if __name__ == "__main__":
    unittest.main()
