import pandas as pd
import json
import pathlib
from raga import *
import pandas as pd
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    parts = x.split("-")
    parts.pop()
    video = "-".join(parts)
    image = x.split("-")
    number = image[-1]
    image.pop()
    image = "-".join(parts)
    return StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/Hb.json/data_points/{video}/images/img_{image}_{number}")

def annotation_v1(row):
    AnnotationsV1 = ImageDetectionObject()
    for index, detection in enumerate(row["detections"]):
        AnnotationsV1.add(ObjectDetection(Id=index, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
    return AnnotationsV1

def model_inferences(row):
    ModelInferences = ImageDetectionObject()
    for index, detection in enumerate(row["detections"]):
        ModelInferences.add(ObjectDetection(Id=index, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
    return ModelInferences

def imag_vectors_m1(row):
    ImageVectorsM1 = ImageEmbedding()
    for embedding in row["ImageVectorsM1"]:
        ImageVectorsM1.add(Embedding(embedding))
    return ImageVectorsM1

def roi_vectors_m1(row):
    ROIVectorsM1 = ROIEmbedding()
    for embedding in row["ROIVectorsM1"]:
        ROIVectorsM1.add(id=embedding.get("Id"), embedding_values=embedding.get("embedding"))
    return ROIVectorsM1

def make_video_id(x):
    return StringElement(pathlib.Path(x).name)


def make_frame_number(x):
    x_split = x.split("_")
    frame = pathlib.Path(x_split[-1]).stem
    return StringElement(int(frame))

# Replace 'your_json_file.json' with the path to your JSON file
json_file_path = './assets/embeddings.json'

# Open the JSON file and read its contents
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

videos = []
videos_embd = []
for item in data:
    video = item['inputs'][0]
    if video not in videos:
        videos.append(item)

emb = pd.DataFrame(videos)
modela = pd.read_json("./assets/model1.json")
modelb = pd.read_json("./assets/model2.json")
emb = emb.explode('inputs')
modela = modela.explode('inputs')
modelb = modelb.explode('inputs')


# Merge the DataFrames on 'key' column one by one
merged_df = pd.merge(emb, modela, on='inputs', suffixes=('_emb','_modela'))
df = pd.merge(merged_df, modelb, on='inputs', suffixes=('_org', '_modelb'))

# df.head(10).to_json("./assets/lm_emb.json")


data_frame = pd.DataFrame()
data_frame["ImageId"] = df["outputs_emb"].apply(lambda x: StringElement(x[0].get('imageName')))
data_frame["Frame"] = df["outputs_emb"].apply(lambda x: make_frame_number(x[0].get('imageName')))
data_frame["VideoId"] = df["inputs"].apply(lambda x: make_video_id(x))
data_frame["ImageUri"] = df["outputs_emb"].apply(lambda x: img_url(x[0].get('imageName')))
data_frame["SourceLink"] = df["outputs_emb"].apply(lambda x: StringElement(x[0].get('imageName')))
data_frame["TimeOfCapture"] = df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
data_frame["weather"] = df["attributes_org"].apply(lambda x: StringElement(x.get("weather")))
data_frame["time_of_day"] = df["attributes_org"].apply(lambda x: StringElement(x.get("time_of_day")))
data_frame["scene"] = df["attributes_org"].apply(lambda x: StringElement(x.get("scene")))
data_frame["ModelA"] = df.apply(lambda x: annotation_v1(x), axis=1)
# data_frame["ModelB"] = df["outputs"].apply(lambda x: model_inferences(x))
# data_frame["ImageVectorsM1"] = df["outputs_emb"].apply(lambda x: imag_vectors_m1(x))
print(data_frame)


