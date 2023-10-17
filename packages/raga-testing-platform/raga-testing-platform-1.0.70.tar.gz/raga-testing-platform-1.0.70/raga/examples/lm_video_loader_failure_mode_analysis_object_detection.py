import pathlib
from raga import *
import pandas as pd
import json
import datetime
import random

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    return StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/Hb.json/data_points/{pathlib.Path(x).stem}/{x}")
    



def model_a_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=frame["time_offset_ms"], detections=detections))

    return model_a_inference


def model_b_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["new_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=frame["time_offset_ms"], detections=detections))

    return model_a_inference

def json_parser(model1, model2):
    model1_df = pd.read_json(model1)
    model2_df = pd.read_json(model2)
    model1_df_exploded = model1_df.explode('inputs')
    model2_df_exploded = model2_df.explode('inputs')
    attributes = model2_df["attributes"].apply(pd.Series)
    model2_df_exploded = pd.concat([model2_df_exploded, attributes], axis=1)
    model2_df_exploded.rename(columns={"outputs": "new_outputs"}, inplace=True)
    merged_df = pd.merge(model1_df_exploded, model2_df_exploded, on='inputs')
    data_frame = pd.DataFrame()
    data_frame["videoId"] = merged_df["inputs"].apply(lambda x: StringElement(pathlib.Path(x).stem))
    data_frame["videoUri"] = merged_df["inputs"].apply(lambda x: img_url(x))
    data_frame["timeOfCapture"] = merged_df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["sourceLink"] = merged_df["inputs"].apply(lambda x: StringElement(x))
    data_frame["dutyType"] = merged_df["dutyType"].apply(lambda x: StringElement(x))
    data_frame["timeOfDay"] = merged_df["time_of_day"].apply(lambda x: StringElement(x))
    data_frame["weather"] = merged_df["weather"].apply(lambda x: StringElement(x))
    data_frame["scene"] = merged_df["scene"].apply(lambda x: StringElement(x))
    data_frame["tags"] = merged_df["tags"].apply(lambda x: StringElement(x))
    data_frame["modelAInference"] = merged_df.apply(model_a_inference, axis=1)
    data_frame["modelBInference"] = merged_df.apply(model_b_inference, axis=1)
    return data_frame




pd_data_frame = json_parser("assets/modelAnew.json", "assets/modelBnew.json")

# print(data_frame_extractor(pd_data_frame).to_csv("assets/testing_data_frame_video_10.csv"))


schema = RagaSchema()
schema.add("videoId", PredictionSchemaElement())
schema.add("videoUri", ImageUriSchemaElement())
schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
schema.add("sourceLink", FeatureSchemaElement())
schema.add("dutyType", AttributeSchemaElement())
schema.add("timeOfDay", AttributeSchemaElement())
schema.add("weather", AttributeSchemaElement())
schema.add("scene", AttributeSchemaElement())
schema.add("tags", AttributeSchemaElement())
schema.add("modelAInference", VideoInferenceSchemaElement(model="modelA"))
schema.add("modelBInference", VideoInferenceSchemaElement(model="modelB"))

run_name = f"lm_video_loader_failure_mode_analysis_object_detection-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

creds = DatasetCreds(arn="arn:aws:iam::527593518644:role/s3-role")
#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session,
                  name="lm-hb-video-ds-v12",
                  type=DATASET_TYPE.VIDEO,
                  data=pd_data_frame,
                  schema=schema,
                  creds=creds,
                  parent_dataset="lm-hb-image-ds-v12")

#load schema and pandas data frame
test_ds.load()