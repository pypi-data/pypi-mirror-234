import csv
import pathlib
from raga import *
import pandas as pd
import json
import datetime
import random

label_to_classname = {
    0: "no_data",
    1: "water",
    2: "trees",
    3: "grass",
    4: "flooded vegetation",
    5: "crops",
    6: "scrub",
    7: "built_area",
    8: "bare_ground",
    9: "snow_or_ice",
    10: "clouds",
}


def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def generate_random_float_list(length=18, min_value=0.0, max_value=500):
    if length <= 10:
        raise ValueError("Length should be greater than 10")
    random_list = [round(random.uniform(min_value, max_value),1) for _ in range(length)]
    return random_list

def parser():
    csv_file_path = "assets/final_image_loss.csv"

    csv_data = pd.read_csv(csv_file_path)
    df = []
    for index, row in csv_data.iterrows():
        if row["label"] in label_to_classname:
            Annotations = SemanticSegmentationObject()
            Loss = LossValue()
            filepath = row["filepath"]
            loss = row["loss"]
            label = label_to_classname[row["label"]]
            Annotations.add(SemanticSegmentation(Id=row["label"], ClassId=0, Segmentation=generate_random_float_list(),  ClassName=label, Format="xn,yn_normalised", Confidence=1))
            Loss.add(id=row["label"], values = loss)
            data_point = {
                'ImageId': StringElement(filepath),
                'ImageUri': StringElement(f"https://raga-test-bucket.s3.ap-south-1.amazonaws.com/1/satsure/data_points/{pathlib.Path(filepath).stem}/images/{filepath}"),
                'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(index)),
                'SourceLink': StringElement(filepath),
                'Annotations': Annotations,
                'LossValue':Loss
            }
            df.append(data_point)
    return pd.DataFrame(df)


# print(data_frame_extractor(parser()).to_csv("satsure.csv"))

pd_data_frame = parser()
schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Annotations", SemanticSegmentationSchemaElement(), pd_data_frame)
schema.add("LossValue", LossValueSchemaElement(), pd_data_frame)

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject",run_name= "labelling-dataset-run-23-aug-v1")

# # #create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name="labelling-dataset-23-aug-v1")

# #load schema and pandas data frame
test_ds.load(data=pd_data_frame, schema=schema)