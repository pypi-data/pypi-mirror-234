
import logging
import os
import pandas as pd
import requests
import zipfile

from raga.raga_schema import VideoDetectionObject


logger = logging.getLogger(__name__)


class FileUploadError(Exception):
    pass

def check_key_value_existence(column_list, key, value):
    return any(column.get(key) == value for column in column_list)

def data_frame_extractor(test_df: pd.DataFrame):
    extracted_df = test_df.applymap(lambda element: element.get())
    return extracted_df

def make_arg(model_name, inference_col_name, embedding_col_name):
    payload = [
        {"customerColumnName": "file_name", "type": "imageName", "modelName": "", "ref_col_name": ""},
        {"customerColumnName": "coco_url", "type": "imageUri", "modelName": "", "ref_col_name": ""},
        {"customerColumnName": "date_captured", "type": "timestamp", "modelName": "", "ref_col_name": ""},
        {"customerColumnName": f"{inference_col_name}_{model_name}", "type": "inference", "modelName": model_name, "ref_col_name": ""},
    ]
    if embedding_col_name:
        payload.append({"customerColumnName": f"{embedding_col_name}_{model_name}", "type": "imageEmbedding", "modelName": model_name, "ref_col_name": ""})
    return payload


def upload_file(pre_signed_url, file_path, success_callback=None, failure_callback=None):
    """
    Uploads a file to the server using a pre-signed URL.

    Args:
        pre_signed_url (str): The pre-signed URL for uploading the file.
        file_path (str): The path of the file to be uploaded.
        success_callback (Optional[function]): The callback function to be called on successful upload.
        failure_callback (Optional[function]): The callback function to be called on upload failure.

    Raises:
        ValueError: If the pre-signed URL or file path is missing.
        FileUploadError: If there is an error uploading the file.
    """
    if not pre_signed_url:
        raise ValueError("Pre-signed URL is required.")
    if not file_path:
        raise ValueError("File path is required.")
    if not os.path.isfile(file_path):
        raise ValueError(f"Invalid file path: {file_path}.")
    logger.debug(f"UPLOADING {file_path}")
    try:
        with open(file_path, "rb") as file:
            response = requests.put(pre_signed_url, data=file, headers={"Content-Type": "application/zip"})
            response.raise_for_status()  # Raise an exception for HTTP errors
            if response.status_code == 200:
                if success_callback:
                    success_callback()
                return True
            else:
                if failure_callback:
                    failure_callback(response.status_code)
                raise FileUploadError(f"File upload failed with status code: {response.status_code}")
    except requests.RequestException as e:
        if failure_callback:
            failure_callback(str(e))
        raise FileUploadError(f"Error uploading file: {e}")


def create_csv_and_zip_from_data_frame(data_frame:pd.DataFrame, csv_file, zip_file):
        """
        Creates a CSV file from the data frame and compresses it into a zip file.
        """
        # Validate the CSV file path
        if not csv_file or not isinstance(csv_file, str):
            raise ValueError(
                "Invalid CSV file path. Please provide a valid file path.")

        # Save the DataFrame as a CSV file
        data_frame.to_csv(csv_file, index=False)
        logger.debug("Data frame has been saved to CSV")

        # Create a zip file containing the CSV file
        with zipfile.ZipFile(zip_file, "w") as zip_file:
            zip_file.write(csv_file, os.path.basename(csv_file))

        logger.debug(f"CSV file has been zipped: {zip_file}")
        print(f"CSV file has been zipped: {zip_file}")


def delete_files(csv_file, zip_file):
    """
    Deletes the CSV and zip files associated with the dataset.
    """
    if os.path.exists(csv_file):
        os.remove(csv_file)
        logger.debug("CSV file deleted")
    else:
        logger.debug("CSV file not found")
        raise FileNotFoundError("CSV file not found.")

    if os.path.exists(zip_file):
        os.remove(zip_file)
        logger.debug("Zip file deleted")
    else:
        logger.debug("Zip file not found")
        raise FileNotFoundError("Zip file not found.")
    return True

def on_upload_success():
    """
    Callback function to be called on successful file upload.
    """
    logger.debug("File uploaded successfully")
    print("File uploaded successfully")

def on_upload_failed(error):
    """
    Callback function to be called on file upload failure.
    """
    logger.debug(f"ERROR: {error}")
    print("File upload failed")