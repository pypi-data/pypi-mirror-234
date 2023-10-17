from raga.validators.dataset_creds_validations import DatasetCredsValidator
from raga.utils import HTTPClient

class DatasetCreds:
    def __init__(self, arn:str):
        self.arn = arn