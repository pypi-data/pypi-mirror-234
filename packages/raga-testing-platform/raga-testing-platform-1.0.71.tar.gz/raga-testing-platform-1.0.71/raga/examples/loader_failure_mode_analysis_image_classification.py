import ast
from raga import *
import pandas as pd
import json
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    return StringElement(f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/signzy/{x.replace('./', '')}")

def model_a_inference(row):
    classification = ImageClassificationElement()
    try:
        confidence = ast.literal_eval(row['ModelA Inference'])
        classification.add("live", confidence.get('live'))
    except Exception as exc:
        classification.add("live", 0)
    return classification


def model_b_inference(row):
    classification = ImageClassificationElement()
    try:
        confidence = ast.literal_eval(row['ModelB Inference'])
        classification.add("live", confidence.get('live'))
    except Exception as exc:
        classification.add("live", 0)
    return classification


def model_gt_inference(row):
    classification = ImageClassificationElement()
    try:
        confidence = ast.literal_eval(row['Ground Truth'])
        classification.add("live", confidence.get('live'))
    except Exception as exc:
        classification.add("live", 0)
    return classification

def image_vectors_m1(row):
    ImageVectorsM1 = ImageEmbedding()
    for embedding in json.loads(row['ImageVectorsM1']):
        ImageVectorsM1.add(Embedding(embedding))
    return ImageVectorsM1


def csv_parser(csv_file):
    df = pd.read_csv(csv_file)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["ImageId"].apply(lambda x: StringElement(x))
    data_frame["ImageUri"] = df["SourceLink"].apply(lambda x: img_url(x))
    data_frame["TimeOfCapture"] = df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["Reflection"] = df.apply(lambda row: StringElement("Yes"), axis=1)
    data_frame["Overlap"] = df.apply(lambda row: StringElement("No"), axis=1)
    data_frame["CameraAngle"] = df.apply(lambda row: StringElement("Yes"), axis=1)
    data_frame["SourceLink"] = df["SourceLink"].apply(lambda x: StringElement(x))
    data_frame["ModelA Inference"] = df.apply(model_a_inference, axis=1)
    data_frame["ModelB Inference"] = df.apply(model_b_inference, axis=1)
    data_frame["Ground Truth"] = df.apply(model_gt_inference, axis=1)
    data_frame["ImageVectorsM1"] =  df.apply(image_vectors_m1, axis=1)
    return data_frame


pd_data_frame = csv_parser("./assets/signzy_df.csv")

#### Want to see in csv file uncomment line below ####
# data_frame_extractor(pd_data_frame).to_csv("signzy_df_csv.csv", index=False)


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("ModelA Inference", ImageClassificationSchemaElement(model="modelA"))
# schema.add("ModelB Inference", ImageClassificationSchemaElement(model="modelB"))
# schema.add("Ground Truth", ImageClassificationSchemaElement(model="GT"))
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="imageModel"))

run_name = f"loader_failure_mode_analysis_image_classification-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/s3-role")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, 
                  name="live-dataset-a", 
                  type=DATASET_TYPE.IMAGE,
                  data=pd_data_frame, 
                  schema=schema, 
                  creds=cred)

#load schema and pandas data frame
test_ds.load()