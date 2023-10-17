import ast
import random
from raga import *
import pandas as pd
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def csv_parser(csv_path):
    data_frame = pd.read_csv(csv_path)
    df = pd.DataFrame()
    df["ImageId"] = data_frame["image_id"].apply(lambda x: StringElement(x))
    df["ImageUri"] = data_frame['lr_path'].apply(lambda x: StringElement(x))
    df["TimeOfCapture"] = data_frame.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    df["SourceLink"] = data_frame['image_name'].apply(lambda x:StringElement(x))
    df["SuperImageUri"] = data_frame['hr_path'].apply(lambda x: StringElement(x))
    return df


pd_data_frame = csv_parser("./assets/super_resolution_data.csv")

#### Want to see in csv file uncomment line below ####
data_frame_extractor(pd_data_frame).to_csv("./assets/super_resolution_data_test_1.csv")

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("SuperImageUri", BlobSchemaElement())





run_name = f"loader_failure_mode_analysis_semantic_segmentation-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name)
cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/model-distribution")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session,
                  name="super_resolution_data_v1",
                  type=DATASET_TYPE.IMAGE,
                  data=pd_data_frame,
                  schema=schema,
                  creds=cred)

#load to server
test_ds.load()

model_exe_fun = ModelExecutorFactory().get_model_executor(test_session=test_session, 
                                                          model_name="Lightmetrics Embedding Model", 
                                                          version="0.1.2")

df = model_exe_fun.execute(init_args={"device": "cpu", "frame_sampling_rate":1}, 
                        execution_args={"input_columns":{"img_paths":"ImageUri"}, 
                                        "output_columns":{"embedding":"imageEmbedding"},
                                        "column_schemas":{"embedding":ImageEmbeddingSchemaElement(model="Lightmetrics Embedding Model")}}, 
                        data_frame=test_ds)

print(df)
test_ds.load()