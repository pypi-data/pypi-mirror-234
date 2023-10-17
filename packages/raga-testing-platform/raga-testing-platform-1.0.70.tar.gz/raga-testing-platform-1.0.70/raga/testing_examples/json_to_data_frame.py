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

def convert_json_to_data_frame(json_file_path_model_1, json_file_path_model_2, json_file_path_model_3):
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

    # Create a dictionary to store the inputs and corresponding data points
    inputs_dict = {}
    hr = 1
    # Process model_1 data
    for item in model_1:
        inputs = item["inputs"]
        inputs_dict[tuple(inputs)] = item
    
    # Process model_2 data
    for item in model_2:
        inputs = item["inputs"]
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        ImageVectorsM1 = ImageEmbedding()
        for detection in item["outputs"][0]["detections"]:
            AnnotationsV1.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM1.add(Embedding(roi_emb))
            attributes_dict = {}
            attributes = item.get("attributes", {})
            for key, value in attributes.items():
                attributes_dict[key] = StringElement(value)
            image_embeddings = item.get("image_embedding", {})
            for value in image_embeddings:
                ImageVectorsM1.add(Embedding(value))

        merged_item = inputs_dict.get(tuple(inputs), {})
        AnnotationsV2 = ImageDetectionObject()
        ROIVectorsM2 = ROIEmbedding()
        ImageVectorsM2 = ImageEmbedding()
        for detection in merged_item["outputs"][0]["detections"]:
            AnnotationsV2.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM2.add(Embedding(roi_emb))
        
        image_embeddings = merged_item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM2.add(Embedding(value))

        data_point = {
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
            'SourceLink': StringElement(item["inputs"][0]),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
            'AnnotationsV2': AnnotationsV2,
            'ROIVectorsM2': ROIVectorsM2,
            'ImageVectorsM2': ImageVectorsM2,
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1

    return test_data_frame



#Convert JSON dataset to pandas Data Frame
pd_data_frame = pd.DataFrame(convert_json_to_data_frame("test-dataset-modelA.json", "test-dataset-modelB.json", "test-dataset-modelG.json"))

pd_data_frame.to_pickle("TestingDataFrame.pkl")