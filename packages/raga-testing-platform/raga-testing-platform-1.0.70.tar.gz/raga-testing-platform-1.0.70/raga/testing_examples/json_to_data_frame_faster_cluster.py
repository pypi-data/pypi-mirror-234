import ast
import csv
import pathlib
import re
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

def convert_json_to_data_frame(json_file_path_model_1, json_file_path_model_2, json_file_path_model_3, embeddings_file=None):
    test_data_frame = []
    with open(json_file_path_model_1, 'r') as json_file:
        # Load JSON data
        model_1 = json.load(json_file)
    with open(json_file_path_model_2, 'r') as json_file:
        # Load JSON data
        model_2 = json.load(json_file)
    
    with open(json_file_path_model_3, 'r') as json_file:
        # Load JSON data
        model_gt = json.load(json_file)
    if embeddings_file:
        with open(embeddings_file, 'r') as json_file:
            # Load JSON data
            embeddings_json = json.load(json_file)

    # Create a dictionary to store the inputs and corresponding data points
    inputs_dict_model_1 = {}
    hr = 1
    # Process model_1 data
    for item in model_1:
        inputs = item["inputs"]
        inputs_dict_model_1[tuple(inputs)] = item
    
    inputs_dict_model_3 = {}
    # Process model_3 data
    for item in model_gt:
        inputs = item["inputs"]
        inputs_dict_model_3[tuple(inputs)] = item

    
    inputs_dict_emb = {}
    # Process emb data
    for item in embeddings_json:
        inputs = item["inputs"]
        inputs_dict_emb[tuple(inputs)] = item

    # Process model_2 data
    for main_index, item in enumerate(model_2):
        ModelAImageClassification = ImageClassificationElement()
        ModelBImageClassification = ImageClassificationElement()
        ModelGImageClassification = ImageClassificationElement()
        inputs = item["inputs"]
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        for index, detection in enumerate(item["outputs"][0]["detections"]):
            id = index+1
            if detection['roi_embedding']:
                print('ROI3')
                ROIVectorsM1.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])

            attributes_dict = {}
            attributes = item.get("attributes", {})
            for key, value in attributes.items():
                attributes_dict[key] = StringElement(value)
        merged_item = inputs_dict_model_1.get(tuple(inputs), {})
        AnnotationsV2 = ImageDetectionObject()
        ROIVectorsM2 = ROIEmbedding()
        for index, detection in enumerate(merged_item["outputs"][0]["detections"]):
            id = index+1
            AnnotationsV2.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=round(random.uniform(0, 1), 1), BBox= [], Format="xywh_normalized"))
            if detection['roi_embedding']:
                print('ROI2')
                ROIVectorsM2.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
        merged_item = inputs_dict_model_3.get(tuple(inputs), {})
        AnnotationsV3 = ImageDetectionObject()
        ROIVectorsM3 = ROIEmbedding()
        for index, detection in enumerate(merged_item["outputs"][0]["detections"]):
            id = index+1
            ModelAImageClassification.add(key=detection['class'], value=round(random.uniform(0, 1), 1))
            ModelGImageClassification.add(key=detection['class'], value=random.randint(0, 1))
            if detection['roi_embedding']:
                print('ROI1')
                ROIVectorsM3.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
        merged_item = inputs_dict_emb.get(tuple(inputs), {})
        ImageVectorsM1 = ImageEmbedding()
        
        image_embeddings = merged_item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM1.add(Embedding(value))

        file_name = os.path.basename(item["inputs"][0])
        data_point = {
            'ImageId': StringElement(file_name),
            'ImageUri': StringElement(f"https://ragaaimedia.s3.ap-south-1.amazonaws.com/54/self_serve-retail_checkout/data_points/{pathlib.Path(file_name).stem}/{file_name}"),
            'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
            'SourceLink': StringElement(file_name),
            'ModelA': ModelAImageClassification,
            'GT': ModelGImageClassification,
            'ModelAROI': ROIVectorsM1,
            'GTROI': ROIVectorsM3,
            'ImageVectorsM1':ImageVectorsM1
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1
        if main_index == 50:
            break
    return test_data_frame

#Convert JSON dataset to pandas Data Frame

# pd_data_frame = pd.DataFrame(convert_json_to_data_frame("assets/mb.json", "assets/ma.json", "assets/gt.json", "assets/ma.json"))

# data_frame_extractor(pd_data_frame).to_pickle("50_images_no_bbox_retail.pkl")

# pd_data_frame = data_frame_extractor(pd.read_pickle("assets/50_images_no_bbox_retail.pkl")).to_csv("assets/50_images_classification.csv", index=False)
# print(pd_data_frame)


# pd_data_frame = pd.read_pickle("assets/50_images_no_bbox_retail.pkl")
pd_data_frame = pd.read_csv("assets/signzy_df.csv")
dr = []
for index, row in pd_data_frame.iterrows():
    df = {}
    try:
        for index_r, column_name in enumerate(pd_data_frame.columns):
            if column_name == "ModelA Inference":
                pass
                # element = row[column_name]
                # conf = ast.literal_eval(element)
                # del conf['spoof']
                # df[column_name] = {'confidence':conf}
            elif column_name == "ModelB Inference":
                element = row[column_name]
                conf = ast.literal_eval(element)
                del conf['spoof']
                df[column_name] = {'confidence':conf}

            elif column_name == "Ground Truth":
                element = row[column_name]
                conf = ast.literal_eval(element)
                del conf['spoof']
                df[column_name] = {'confidence':conf}
                
            elif column_name == "ImageVectorsM1":
                element = row[column_name]
                element = json.loads(element)
                element_value = {'embeddings':element}
                df[column_name] = element_value
            # elif column_name == "Weather":
            #     element = row[column_name]
            #     df[column_name] = None
            # elif column_name == "TimeofDay":
            #     element = row[column_name]
            #     df[column_name] = ""
            elif column_name == "TimeOfCapture":
                element = row[column_name]
                df[column_name] = get_timestamp_x_hours_ago(index_r)
            elif column_name == "ImageId":
                element = row[column_name]
                df[column_name] = element
                df["ImageUri"] = f"https://raga-test-bucket.s3.ap-south-1.amazonaws.com/spoof/{element}"
            else:
                element = row[column_name]
                element_value = element
                df[column_name] = element_value
    except Exception as e:
            continue
    dr.append(df)
pd_data_frame = pd.DataFrame(dr)


pd_data_frame.to_csv("signzy_df_1.csv", index=False)

pd_data_frame = pd.read_csv("signzy_df_1.csv")


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
# schema.add("Weather", AttributeSchemaElement(), pd_data_frame)
# schema.add("TimeofDay", AttributeSchemaElement(), pd_data_frame)
# schema.add("ModelA Inference", ImageClassificationSchemaElement(model="modelA"), pd_data_frame)
schema.add("ModelB Inference", ImageClassificationSchemaElement(model="modelB"), pd_data_frame)
schema.add("Ground Truth", ImageClassificationSchemaElement(model="GT"), pd_data_frame)
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="imageModel"), pd_data_frame)


# create test_session object of TestSession instance
test_session = TestSession(project_name="LivenessDetection", run_name= "run-29-aug-classification-v9", access_key="xOVWFaP2fUB53jJkeflD", secret_key="RdhCitkCBLeq0YhA0VSlrSEeb8nbaVyKALF8dgBB", host="http://13.200.65.88:8080")

# test_session = TestSession(project_name="testingProject", run_name= "run-29-aug-classification-v9", access_key="nnXvot82D3idpraRtCjJ", secret_key="P2doycL4WBZXLNARIs4bESxttzF3MHSC5K15Jrs9", host="http://65.0.13.122:8080")

# # #create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name="live-dataset")

# #load schema and pandas data frame
test_ds.load(data=pd_data_frame, schema=schema)