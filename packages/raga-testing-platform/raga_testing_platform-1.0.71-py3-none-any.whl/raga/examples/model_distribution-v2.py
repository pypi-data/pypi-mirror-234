import ast
import pandas as pd
import json

from raga import *

import datetime

def img_url(x):
    file = x.split("/")[-1]
    return StringElement(f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/selected_coco_images/{file}")

def json_parser(json_file):
    df = pd.read_json(json_file)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["ImageId"].apply(lambda x: StringElement(x))
    data_frame["ImageUri"] = df["SourceLink"].apply(lambda x: img_url(x))
    return data_frame

raga_data_frame = json_parser("./assets/COCO_engg_final_100.csv")


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())

run_name = f"model_distribution-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


test_session = TestSession(project_name="testingProject", run_name= run_name)

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/model-distribution")

raga_dataset = Dataset(test_session=test_session, 
                       name="md-m-test-v1", 
                       data=raga_data_frame, 
                       schema=schema, 
                       type=DATASET_TYPE.IMAGE,
                       creds=cred)
raga_dataset.load()


model_exe_fun = ModelExecutorFactory().get_model_executor(test_session=test_session, 
                                                          model_name="Signzy Embedding Model", 
                                                          version="0.2.2")

model_exe_fun.execute(init_args={"device": "cpu"}, 
                           execution_args={"input_columns":{"img_paths":"ImageUri"}, 
                                           "output_columns":{"embedding":"ImageEmbedding"},
                                           "column_schemas":{"embedding":ImageEmbeddingSchemaElement(model="Signzy Embedding Model")}}, 
                           data_frame=raga_dataset)

raga_dataset.load()