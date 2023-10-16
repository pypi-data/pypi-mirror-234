import ast
from raga import *
import pandas as pd
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def image_classification(x):
    classification = ImageClassificationElement()
    x = ast.literal_eval(x)
    for key, value in x.items():
        classification.add(key=key, value=value)
    return classification

def mistake_score(x):
    mistake_score = MistakeScore()
    x = ast.literal_eval(x)
    for key, value in x.items():
        mistake_score.add(key=key, value=value, area=0)
    return mistake_score

def image_id(index, row):
    file = row["SourceLink"].split("/")[-1]
    return StringElement(f"{index}_{file}".replace(" ", "_"))

def replace_embedding(x):
    embeddings = ImageEmbedding()
    for embedding in x:
        embeddings.add(Embedding(embedding))
    return embeddings

def csv_parser(csv_file, embedding_file):
    df = pd.read_csv(csv_file).head(100)
    embeddings = pd.read_json(embedding_file)
    merged_df = pd.merge(df, embeddings, left_on="SourceLink", right_on="filepath", how="inner")
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = merged_df.apply(lambda x: image_id(x.name, x) , axis=1)
    data_frame["ImageUri"] = merged_df["SourceLink"].apply(lambda x: StringElement(f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1{x.replace('100_sports_dataset', '')}"))
    data_frame["SourceLink"] = merged_df["SourceLink"].apply(lambda x: StringElement(x))
    data_frame["TimeOfCapture"] = merged_df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["GroundTruth"] = merged_df["Ground Truth"].apply(image_classification)
    data_frame["MistakeScore"] = merged_df["mistake_score"].apply(mistake_score)
    data_frame["ImageVectorsM1"] = merged_df['embedding'].apply(lambda x:replace_embedding(x))
    return data_frame

pd_data_frame = csv_parser("./assets/labelling_qc_score_df.csv", "./assets/train.json")

#### Want to see in csv file uncomment line below ####
# data_frame_extractor(pd_data_frame).to_csv("./assets/labelling_qc_score_df_test_embeddings.csv", index=False)

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("GroundTruth", ImageClassificationSchemaElement(model="GT"))
schema.add("MistakeScore", MistakeScoreSchemaElement(ref_col_name="GroundTruth"))
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="imageModel1"))

run_name = f"loader_labeling_quality_image_classification-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
# test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="qGIXoxPVMObBs9DzBXuX", secret_key="VqpODChJcTi3QHWmr4PZiX6D1aXxid7QSd7YKpyJ", host="http://prod-raga.ragaai.in")

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/s3-role")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session,
                  name="100-sport-dataset-100-v2",
                  type=DATASET_TYPE.IMAGE,
                  data=pd_data_frame, 
                  schema=schema, 
                  creds=cred)

#load to server
test_ds.load()