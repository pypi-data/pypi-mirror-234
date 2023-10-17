import os
import time
import requests
from typing import Optional
import pandas as pd
import logging
import zipfile
from raga.constants import INVALID_RESPONSE, INVALID_RESPONSE_DATA


from raga.exception import RagaException
from raga.raga_schema import RagaSchema
from raga.validators.dataset_validations import DatasetValidator
from raga.dataset_creds import DatasetCreds
from raga import TestSession

from raga.utils import (get_file_name, 
                        delete_files, 
                        upload_file, 
                        create_csv_and_zip_from_data_frame, 
                        data_frame_extractor, 
                        make_arg, 
                        on_upload_success, 
                        on_upload_failed, 
                        check_key_value_existence)


logger = logging.getLogger(__name__)


class DatasetException(RagaException):
    pass

class DATASET_TYPE:
    IMAGE = "image"
    VIDEO = "video"
    ROI = "roi"
    EVENT = "event"


class Dataset:
    MAX_RETRIES = 3
    RETRY_DELAY = 1

    def __init__(
        self,
        test_session:TestSession,
        name: str,
        type:str,
        data: (pd.DataFrame, str) = None,
        schema: Optional[RagaSchema] = None,
        creds: Optional[DatasetCreds] = None,
        parent_dataset: Optional[str] = "",
        format: Optional[str] = None,
        model_name: Optional[str] = None,
        inference_col_name: Optional[str] = None,
        embedding_col_name: Optional[str] = None,
        u_test: bool = False
    ):
        self.test_session = test_session
        self.name = DatasetValidator.validate_name(name)
        self.type = DatasetValidator.validate_type(type)
        self.creds = DatasetValidator.validate_creds(creds)
        self.parent_dataset = parent_dataset
        self.csv_file = f"experiment_{test_session.experiment_id}_{self.name}.csv"
        self.zip_file = f"experiment_{test_session.experiment_id}_{self.name}.zip"
        self.dataset_id = None
        
        if not u_test:
            self.dataset_id = self.create_dataset()
            if self.creds and self.dataset_id:
                self.create_dataset_creds()

        self.dataset_file_id = None
        self.data_set_top_five_rows = {}
        self.raga_dataset = data
        self.raga_extracted_dataset = None
        self.raga_schema = schema
        self.dataset_schema_columns = None
        self.format = format
        self.model_name = model_name
        self.inference_col_name = inference_col_name
        self.embedding_col_name = embedding_col_name
        self.parent_dataset_id = self.parent_dataset_validation()
        
        self.init()

    def init(self):
        from raga import EMPTY_DATA_FRAME, INVALID_DATA_ARG, INVALID_SCHEMA

        if isinstance(self.raga_dataset, str):
            self.load_dataset_from_file() # Assume it's a file path
        elif isinstance(self.raga_dataset, pd.DataFrame):
            if self.raga_dataset.empty:
                raise DatasetException(EMPTY_DATA_FRAME)
                
            if self.raga_schema is None:
                raise DatasetException(INVALID_SCHEMA)
            
            if not isinstance(self.raga_schema, RagaSchema):
                raise DatasetException(INVALID_SCHEMA)
            
            self.dataset_schema_columns = self.raga_schema.columns
            self.raga_extracted_dataset = data_frame_extractor(self.raga_dataset)  
        else:
            raise DatasetException(INVALID_DATA_ARG)

    def load(self,  schema: Optional[RagaSchema] = None):
        self.raga_schema = schema if schema else self.raga_schema
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                self.load_data_frame()
                    
                print("Data loaded successful!")
                break  # Exit the loop if initialization succeeds
            except requests.exceptions.RequestException as e:
                print(f"Network error occurred: {str(e)}")
                retries += 1
                if retries < self.MAX_RETRIES:
                    print(f"Retrying in {self.RETRY_DELAY} second(s)...")
                    time.sleep(self.RETRY_DELAY)

    def load_data_frame(self):
        """
        Loads the data frame, creates a CSV file, zips it, and uploads it to the server.
        """
        self.data_frame_validation()
        create_csv_and_zip_from_data_frame(self.raga_extracted_dataset, self.csv_file, self.zip_file)
        signed_upload_path, file_path = self.get_pre_signed_s3_url(self.zip_file)
        upload_file(
            signed_upload_path,
            self.zip_file,
            success_callback=on_upload_success,
            failure_callback=on_upload_failed,
        )
        delete_files(self.csv_file, self.zip_file)

        self.dataset_file_id = self.create_dataset_load_definition(file_path, "csv", self.raga_schema.columns)
        self.notify_server()

    def load_dataset_from_file(self):
        from raga import REQUIRED_ARG
        if not self.format:
            raise DatasetException(f"{REQUIRED_ARG.format('format')}")
        if not self.model_name:
            raise DatasetException(f"{REQUIRED_ARG.format('model_name')}")
        if not self.inference_col_name:
            raise DatasetException(f"{REQUIRED_ARG.format('inference_col_name')}")
            
        file_dir = os.path.dirname(self.raga_dataset)
        file_name_without_ext, file_extension, file_name = get_file_name(
            self.raga_dataset)
        zip_file_name = os.path.join(file_dir, file_name_without_ext + ".zip")

        with zipfile.ZipFile(zip_file_name, "w") as zip_file:
            zip_file.write(self.raga_dataset, file_name)
        signed_upload_path, file_path  = self.get_pre_signed_s3_url(
            file_name_without_ext + ".zip")
        
        upload_file(
            signed_upload_path,
            zip_file_name,
            success_callback=on_upload_success,
            failure_callback=on_upload_failed,
        )
        if os.path.exists(zip_file_name):
            os.remove(zip_file_name)
            logger.debug("Zip file deleted")
        else:
            logger.debug("Zip file not found")

        arguments = make_arg(self.model_name, self.inference_col_name, self.embedding_col_name)

        self.dataset_file_id = self.create_dataset_load_definition(file_path, format, arguments)
        self.notify_server()

    def head(self):
        res_data = self.test_session.http_client.get(
            f"api/dataset/{self.dataset_id}/data",
            headers={"Authorization": f'Bearer {self.test_session.token}'},
        )
        if not res_data or 'data' not in res_data or 'rows' not in res_data['data'] or 'columns' not in res_data['data']:
            raise DatasetException("Record not found!")
        
        print(self.filter_head(res_data.get('data', {}).get('rows', {}), res_data.get('data', {}).get('columns', {})))

    def filter_head(self, rows, columns):
        pd_data = pd.DataFrame(rows)
        columns_temp = []
        for col in columns:
            columns_temp.append(col.get("columnName"))
        return pd_data.get(columns_temp)

    def get_pre_signed_s3_url(self, file_name: str):
        res_data = self.test_session.http_client.get(
            "api/dataset/uploadpath",
            None,{"experimentId": self.test_session.experiment_id, "fileName": file_name, "contentType":"application/zip"},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )
        logger.debug("Pre-signed URL generated")
        print("Pre-signed URL generated")
        return res_data["data"]["signedUploadPath"], res_data["data"]["filePath"]

    def notify_server(self):
        """
        Notifies the server to load the dataset with the provided experiment ID and data definition.
        """
        res_data = self.test_session.http_client.post(
            "api/experiment/load-data",
            {"experimentId": self.test_session.experiment_id, "datasetFileId": self.dataset_file_id},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )
        logger.debug(res_data.get('data', ''))
        return res_data

    def create_dataset(self):
        if not self.test_session.project_id:
            raise DatasetException("Project ID is required.")
        if not self.test_session.token:
            raise DatasetException("Token is required.")

        res_data = self.test_session.http_client.post(
            "api/dataset",
            {"name": self.name, 
             "projectId": self.test_session.project_id, 
             "experimentId":self.test_session.experiment_id,
             "type":self.type,
             "parentDataset":self.parent_dataset},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

        if not res_data or 'data' not in res_data or 'id' not in res_data['data']:
            raise DatasetException("Failed to create dataset.")

        return res_data['data']['id']

    def create_dataset_creds(self,):
        if not self.dataset_id:
            raise DatasetException("Dataset ID is required.")
        if not self.test_session.token:
            raise DatasetException("Token is required.")

        data = {
            "datasetId": self.dataset_id,
            "storageService": "s3",
            "json": {'arn': self.creds.arn}
        }
        res_data = self.test_session.http_client.post(
            "api/dataset/credential",
            data,
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

        if not res_data or 'data' not in res_data or 'id' not in res_data['data']:
            raise DatasetException("Failed to create dataset credentials.")

        return res_data['data']['id']
    
    def create_dataset_load_definition(self, filePath: str, type: str, arguments: dict):
        payload = {
            "datasetId": self.dataset_id,
            "filePath": filePath,
            "type": type,
            "arguments": arguments
        }

        res_data = self.test_session.http_client.post(
            "api/dataset/definition", payload,
            {"Authorization": f'Bearer {self.test_session.token}'},
        )
        return res_data.get('data',{}).get('id')

    def get_data_frame(self, columns:list):
        image_id_column = next((item['customerColumnName'] for item in self.raga_schema.columns if item['type'] == 'imageName'), None)
        if image_id_column not in columns:
            columns.append(image_id_column)
        
        missing_columns = [col for col in columns if col not in self.raga_extracted_dataset.columns]
        if not missing_columns:
            return self.raga_extracted_dataset[columns], image_id_column
        else:
            missing_columns_str = ', '.join(missing_columns)
            raise DatasetException(f"The following columns do not exist in the DataFrame: {missing_columns_str}")

    def set_data_frame(self, data_frame:pd.DataFrame):
        image_id_column = next((item['customerColumnName'] for item in self.raga_schema.columns if item['type'] == 'imageName'), None)
        merged_df = pd.merge(self.raga_extracted_dataset, data_frame, on=image_id_column, how='inner', suffixes=('', '_right'))
        self.raga_extracted_dataset = merged_df
        return 1
    
    def data_frame_validation(self):
        from raga.constants import SCHEMA_KEY_DOES_NOT_EXIST, COL_DOES_NOT_EXIST

        column_list = self.raga_extracted_dataset.columns.to_list()
        for col in self.raga_schema.columns:
            if col.get("customerColumnName") not in column_list:
                raise DatasetException(f"{COL_DOES_NOT_EXIST.format(col.get('customerColumnName'), column_list)}")
            # self.validate_data_frame_value(col, self.raga_extracted_dataset.loc[0,col.get("customerColumnName")])

        if not check_key_value_existence(self.raga_schema.columns, 'type', 'imageName'):
            raise DatasetException(SCHEMA_KEY_DOES_NOT_EXIST)
    
    def validate_data_frame_value(self, col, col_value):
        from raga.constants import DATASET_FORMAT_ERROR

        if col.get('type') == "classification" and "confidence" not in col_value:
                raise DatasetException(f"{DATASET_FORMAT_ERROR.format(col.get('customerColumnName'))}")
        
        if (col.get('type') == "imageEmbedding" or col.get('type') == "roiEmbedding") and "embeddings" not in col_value:
                raise DatasetException(f"{DATASET_FORMAT_ERROR.format(col.get('customerColumnName'))}")
        
        if col.get('type') == "inference" and "detections" not in col_value:
                raise DatasetException(f"{DATASET_FORMAT_ERROR.format(col.get('customerColumnName'))}")
        return 1
    
    def parent_dataset_validation(self):
        if self.parent_dataset:
            res_data = self.test_session.http_client.get(f"api/dataset?projectId={self.test_session.project_id}&name={self.parent_dataset}", headers={"Authorization": f'Bearer {self.test_session.token}'})

            if not isinstance(res_data, dict):
                    raise ValueError(INVALID_RESPONSE)
            dataset_id = res_data.get("data", {}).get("id")

            if not dataset_id:
                raise KeyError(INVALID_RESPONSE_DATA)
            return dataset_id
        return None