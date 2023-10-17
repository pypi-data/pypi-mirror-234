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


def parseLossFile(csv_file_path):
    df = pd.read_csv(csv_file_path)
    f2l = {}
    file_paths = []
    for index, row in df.iterrows():

        if row['label'] not in label_to_classname:
            continue

        file_path = row['filepath']
        if file_path not in f2l:
            file_paths.append(file_path)
            f2l[file_path] = []
        f2l[file_path].append([row['label'], row['loss']])

    return file_paths, f2l


def generate_data_frame(file_paths, f2l):
    data = []
    for filepath in file_paths:

        annotations = SemanticSegmentationObject()
        loss_values = LossValue()

        for i, item in enumerate(f2l[filepath]):
            if item[0] not in label_to_classname:
                continue
            label = label_to_classname[item[0]]
            segmentation = generate_random_float_list()
            annotations.add(SemanticSegmentation(Id=i, ClassId=item[0], ClassName=label, Segmentation=segmentation, Confidence=1, Format="xn,yn_normalised"))
            loss_values.add(id=i, values=item[1])

        image_url = f"https://raga-test-bucket.s3.ap-south-1.amazonaws.com/1/satsure/data_points/{pathlib.Path(filepath).stem}/images/{filepath}"
        timestamp = get_timestamp_x_hours_ago(i)
        data_point = {
            'ImageId': StringElement(filepath),
            'ImageUri': StringElement(image_url),
            'TimeOfCapture': TimeStampElement(timestamp),
            'SourceLink': StringElement(filepath),
            'Annotations': annotations,
            'LossValue': loss_values,
            'Reflection': StringElement('Yes'),
            'Overlap': StringElement('Yes'),
            'CameraAngle': StringElement('Top')
        }
        data.append(data_point)

    return pd.DataFrame(data)


csv_file_path = "./assets/final_image_loss_test.csv"
dataset_name = "satsure-dataset"
experiment_name = "satsure-aug-30-v1"

file_paths, f2l = parseLossFile(csv_file_path)
df = generate_data_frame(file_paths, f2l)


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), df)
schema.add("ImageUri", ImageUriSchemaElement(), df)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), df)
schema.add("SourceLink", FeatureSchemaElement(), df)
schema.add("Annotations", SemanticSegmentationSchemaElement(), df)
schema.add("LossValue", LossValueSchemaElement(), df)
schema.add('Reflection', AttributeSchemaElement(), df)
schema.add('Overlap', AttributeSchemaElement(), df)
schema.add('CameraAngle', AttributeSchemaElement(), df)

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name=experiment_name)

# # #create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name=dataset_name)

# #load schema and pandas data frame
test_ds.load(data=df, schema=schema)