import logging
import os
import subprocess
import sys
import requests
from urllib.parse import urlparse, unquote
from raga.constants import INVALID_DATASET, INVALID_EXECUTION_ARG, INVALID_INIT_ARG, INVALID_RESPONSE, INVALID_RESPONSE_DATA, INVALID_RESPONSE_MODEL_ID_NOT_FOUND, MODEL_LIB_NOT_FOUND, MODEL_OR_PYTHON_NOT_FOUND, MODEL_REQUIRED_NOT_EMPTY, MODEL_VERSION_REQUIRED_NOT_EMPTY, PLATFORM_NOT_SUPPORT, PYTHON_NOT_SUPPORT, WHEEL_INSTALL_FAIL, WHEEL_NOT_FOUND, WHEEL_UNINSTALL_FAIL


from raga.dataset import Dataset
from raga.exception import RagaException
from raga.test_session import TestSession
from raga.utils.raga_config_reader import format_python_versions, get_machine_platform, get_python_version, get_config_file_path

logger = logging.getLogger(__name__)

RAGA_REPO_PATH = ".raga/raga_repo"
MODEL_PATH = "models"

class ModelExecutorFactoryException(RagaException):
    pass

class PlatformError(RagaException):
    pass

class PythonVersionError(RagaException):
    pass

class WheelFileInstallationError(RagaException):
    pass

class ModelExecutorError(RagaException):
    pass

class ModelExecutor:
    def __init__(self, executor, wheel_path):
        self.executor = executor
        self.wheel_file_path = wheel_path

    def execute(self, init_args, execution_args, data_frame:Dataset):
        execution_validation(init_args=init_args, execution_args=execution_args, dataset=data_frame)
        try:
            auth = {'aws_access_key_id': data_frame.test_session.aws_raga_access, 'aws_secret_access_key': data_frame.test_session.aws_raga_secret}
            role = data_frame.test_session.aws_raga_arn
            self.executor.initialise(init_args, role, auth)
            columns = list(execution_args.get('input_columns').values())
            column_keys = list(execution_args.get('output_columns').keys())
            column_schema = execution_args.get('column_schemas')
            for item in column_keys:
                col = execution_args['output_columns'][item]
                data_frame.raga_schema.add(col, column_schema[item])
            df = data_frame.get_data_frame(columns)[0]
            role = data_frame.creds.arn
            df = self.executor.run(data_frame=df, input_args=execution_args['input_columns'], output_args=execution_args['output_columns'], role=role, auth=auth)
            data_frame.set_data_frame(df)
            uninstall_wheel(self.wheel_file_path)
            return df
        except Exception as exc:
            logger.exception(exc)
            uninstall_wheel(self.wheel_file_path)
            sys.exit(1)


class ModelExecutorFactory:
    @classmethod
    def get_model_executor(cls, test_session:TestSession, model_name:str, version:str):
        if not isinstance(model_name, str) or not model_name:
            raise ModelExecutorFactoryException(MODEL_REQUIRED_NOT_EMPTY)
        if not isinstance(version, str) or not version:
            raise ModelExecutorFactoryException(MODEL_VERSION_REQUIRED_NOT_EMPTY)
        
        model_api_client = ModelAPIClient(test_session)

        local_platform = get_machine_platform()
        local_python_version = get_python_version()
        
        model_id = model_api_client.get_model_id(model_name=model_name)
        model_version = model_api_client.get_version_by_version(model_id=model_id, version=version, platform=local_platform, python=local_python_version)

        model_wheel =  model_validation(model_version, model_name, RAGA_REPO_PATH, MODEL_PATH)
        wheel_path = download_model(model_wheel)
        # wheel_path = "/home/ubuntu/developments/Embedding-Generator-Package-Lightmetrics/dist/raga_models-0.1.2-cp311-cp311-linux_x86_64.whl"
        # wheel_path = "/home/ubuntu/developments/Embedding-Generator-Package/dist/raga_models-0.1.1-cp311-cp311-linux_x86_64.whl"
        install_wheel(wheel_path)
        try:
            from raga_models.executor import Executor
            executor = Executor()
            return ModelExecutor(executor, wheel_path)
        except ImportError:
            raise ModelExecutorError(MODEL_LIB_NOT_FOUND)
    

    
class ModelAPIClient:
    def __init__(self, test_session=TestSession):
        self.http_client = test_session.http_client

        self.token = test_session.token
        self.project_id = test_session.project_id
        self.experiment_id = test_session.experiment_id


    def get_model_id(self, model_name):
        res_data = self.http_client.get(
            "api/model",
            params={"modelName": model_name, "projectId":self.project_id},
            headers={"Authorization": f'Bearer {self.token}'},
        )

        if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)

        model_id = res_data.get("data", {}).get('id')

        if not model_id:
            raise KeyError(INVALID_RESPONSE_MODEL_ID_NOT_FOUND)
        return model_id
    

    def get_version_by_version(self, model_id, version, platform, python):
        res_data = self.http_client.get(
            "api/models-version",
            params={
                "modelId": model_id,
                "version":version,
                "pythonVersion":python, 
                "platform":platform
                },
            headers={"Authorization": f'Bearer {self.token}'},
        )

        if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)

        data = res_data.get("data", {})

        if not data:
            raise KeyError(INVALID_RESPONSE_DATA)
        return data
    

def execution_validation(init_args: dict, execution_args: dict, dataset: Dataset):
    if not isinstance(dataset, Dataset):
        raise ModelExecutorFactoryException(INVALID_DATASET)
    
    if not isinstance(init_args, dict):
        raise ModelExecutorFactoryException(INVALID_INIT_ARG)
    
    if not isinstance(execution_args, dict):
        raise ModelExecutorFactoryException(INVALID_EXECUTION_ARG)
    return 1


def model_validation(model, model_name, raga_repo_path, model_path):

    if not model.get("wheelFile"):
        raise ModelExecutorFactoryException(WHEEL_NOT_FOUND)

    raga_models_path = os.path.join(get_config_file_path(raga_repo_path), f"{model_path}/{model_name}/{model.get('version')}")
    if not os.path.exists(raga_models_path):
        os.makedirs(raga_models_path)
    model["raga_models_path"] = raga_models_path
    whl_files = os.listdir(raga_models_path)
    if any(file.endswith('.whl') for file in whl_files): 
        model["whl_path"] = raga_models_path
    return model

def get_wheel_file_name(model):
    wheel_file_url = model.get("wheelFile")
    parts = wheel_file_url.split()
    file_path = parts[-1]
    parsed_file_path = urlparse(file_path)
    return unquote(parsed_file_path.path.split("/")[-1])

def download_model(model):
    wheel_file = model.get("wheelFile")
    if model.get("whl_path"):
        model_wheel = os.path.join(model.get("whl_path"), get_wheel_file_name(model))
    else:
        model_wheel = os.path.join(model.get('raga_models_path'),get_wheel_file_name(model))
        with requests.get(wheel_file, stream=True) as response:
            response.raise_for_status()
            with open(model_wheel, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    return model_wheel


def install_wheel(package_name):
    try:
        logger.debug(f"PIP INSTALLING {package_name}")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, capture_output
        =True)
        logger.debug(f"PIP INSTALLED {package_name}")
    except subprocess.CalledProcessError as e:
        raise WheelFileInstallationError(f"{WHEEL_INSTALL_FAIL} {package_name}. Error: {e}")

def uninstall_wheel(package_name):
    try:
        logger.debug(f"PIP UNINSTALLING {package_name}")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", package_name, "-y"], check=True, capture_output=True)
        logger.debug(f"PIP UNINSTALLED {package_name}")
    except subprocess.CalledProcessError as e:
        raise WheelFileInstallationError(f"{WHEEL_UNINSTALL_FAIL} {package_name}. Error: {e}")