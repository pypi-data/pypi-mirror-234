import pathlib
from raga import *
import pandas as pd
import datetime
import numpy as np
from faker import Faker

label_to_classname = {
    1: "no_data",
    2: "water",
    3: "trees",
    4: "grass",
    5: "flooded vegetation",
    6: "crops",
    7: "scrub",
    8: "built_area",
    9: "bare_ground",
    10: "snow_or_ice",
    11: "clouds",
}

def generate_fake_image_embedding(embedding_dimension):
    """
    Generate a single fake image embedding.

    Args:
        embedding_dimension (int): Dimensionality of the embedding.

    Returns:
        A fake image embedding as a NumPy array.
    """
    # Generate a random fake image embedding vector
    fake_embedding = np.random.rand(embedding_dimension)
    embeddings = ImageEmbedding()
    for embedding in fake_embedding:
        # print(embedding)
        embeddings.add(Embedding(embedding))
    return embeddings

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def image_url(x):
    return f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/GrassLands_image/{pathlib.Path(x).name}"

def mask_url(x):
    return f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/GrassLands/{pathlib.Path(x).name}"

def attached_label(id, loss):
    return {id:loss}

def merge_loss_dicts(loss_dicts):
    mistake_score = MistakeScore()
    for d in loss_dicts:
        for key, value in d.items():
            mistake_score.add(key=key, value=value)
    return mistake_score

def csv_parser(file_path):
    df = pd.read_csv(file_path)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["ImageId"].apply(lambda x: StringElement(x))
    data_frame["ImageUri"] = df["SourceLink"].apply(lambda x: StringElement(image_url(x)))
    data_frame["TimeOfCapture"] = df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["SourceLink"] = df['SourceLink'].apply(lambda x:StringElement(x))
    data_frame["Annotations"] = df['Annotations'].apply(lambda x:StringElement(mask_url(x)))
    # data_frame["ImageEmbedding"] = df.apply(lambda x: generate_fake_image_embedding(80), axis=1)
    return data_frame

data_frame = csv_parser("./assets/GrassLands.csv")
# data_frame = csv_parser("./assets/GrassLands.csv")

#### Want to see in csv file uncomment line below ####
# data_frame_extractor(data_frame).to_csv("./assets/final_image_loss_full_s_df_new_1_image.csv", index=False)

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("Annotations", TIFFSchemaElement(label_mapping=label_to_classname, schema="tiff"))
# schema.add("ImageEmbedding", ImageEmbeddingSchemaElement(model="imageModel"))



run_name = f"loader_lq_ss-drift-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name = run_name)

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/model-distribution")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, 
                  name="GrassLands-v4", 
                  type=DATASET_TYPE.IMAGE,
                  data=data_frame, 
                  schema=schema, creds=cred)

# #load schema and pandas data frame
test_ds.load()


model_exe_fun = ModelExecutorFactory().get_model_executor(test_session=test_session, 
                                                          model_name="Satsure Embedding Model", 
                                                          version="0.2.0")

model_exe_fun.execute(init_args={"device": "cpu"}, 
                           execution_args={"input_columns":{"img_paths":"ImageUri"}, 
                                           "output_columns":{"embedding":"ImageEmbedding"},
                                           "column_schemas":{"embedding":ImageEmbeddingSchemaElement(model="Satsure Embedding Model")}}, 
                           data_frame=test_ds)

test_ds.load()
