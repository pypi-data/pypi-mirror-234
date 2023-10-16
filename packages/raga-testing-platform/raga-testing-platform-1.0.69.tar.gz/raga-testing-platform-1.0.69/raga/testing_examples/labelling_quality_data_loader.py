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

def generate_random_float_list(length=18, min_value=0.0, max_value=500):
    if length <= 10:
        raise ValueError("Length should be greater than 10")
    random_list = [round(random.uniform(min_value, max_value),1) for _ in range(length)]
    return random_list


def generate_random_roadside_class():
    classes = [
        "fruits",
        "vegetables",
        "dairy products",
        "meat",
        "seafood",
        "canned goods",
        "bakery items",
        "beverages",
        "snacks",
        "cereals",
        "spices",
        "frozen foods",
        "deli items",
        "cleaning supplies",
        "personal care",
        "household essentials",
        "pet supplies",
        "baby care",
        "health and wellness",
        "condiments"
        # Add more classes as needed
    ]
    return random.choice(classes)

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
        Annotations = SemanticSegmentationObject()
        Loss = LossValue()
        inputs = item["inputs"]
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        for index, detection in enumerate(item["outputs"][0]["detections"]):
            id = index+1
            Annotations.add(SemanticSegmentation(Id=id, ClassId=0, Segmentation=generate_random_float_list(),  ClassName=generate_random_roadside_class(), Format="xn,yn_normalised", Confidence=1))
            Loss.add(id=id, values = round(random.uniform(0, 1), 1))
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
            'Reflection':StringElement('Yes'),
            'Overlap':StringElement('No'),
            'CameraAngle':StringElement('Top'),
            'Annotations': Annotations,
            'LossValue':Loss
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1
        if main_index == 50:
            break
    return test_data_frame

#Convert JSON dataset to pandas Data Frame

pd_data_frame = pd.DataFrame(convert_json_to_data_frame("assets/mb.json", "assets/ma.json", "assets/gt.json", "assets/ma.json"))

# print(data_frame_extractor(pd_data_frame).to_csv("updated_lqt.csv"))
schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
schema.add("Annotations", SemanticSegmentationSchemaElement(), pd_data_frame)
schema.add("LossValue", LossValueSchemaElement(), pd_data_frame)

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject",run_name= "lqt-run-18-aug-v1")

# # #create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name="labelling-dataset-18-aug-v1")

# #load schema and pandas data frame
test_ds.load(data=pd_data_frame, schema=schema)