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

def convert_json_to_data_frame(embeddings_file, dataset):
    with open(embeddings_file, 'r') as json_file:
        # Load JSON data
        embeddings_json = json.load(json_file)
    test_data_frame = []
    hr = 1
    for item in embeddings_json:
        attr = item.get('attributes', {})
        attributes_dict = {}
        for key, value in attr.items():
            attributes_dict[key] = StringElement(value)
        if attr.get("dataset_type", None) == dataset:
            print(dataset)
            ImageVectorsM1 = ImageEmbedding()
            image_embeddings = item.get("image_embedding", {})
            for value in image_embeddings:
                ImageVectorsM1.add(Embedding(value))

            file_name = os.path.basename(item["inputs"][0])
            data_point = {
                'ImageId': StringElement(file_name),
                'ImageUri': StringElement(f"https://nusceneraga.s3.ap-south-1.amazonaws.com/nuscene_rainy_images/{file_name}"),
                'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
                'SourceLink': StringElement(file_name),
                'ImageEmbedding': ImageVectorsM1,
            }
            merged_dict = {**data_point, **attributes_dict}
            test_data_frame.append(merged_dict)
            hr+=1
            
    return test_data_frame
# convert_json_to_data_frame("nuscene_US_rainy_clear_engg_embedding.json", "field_data/train-data")
# print(len(convert_json_to_data_frame("ModelA_faster_rcnn_r50_fpn_nuscene_US_rainy_clear_engg_embedding.json", "train-data")))


#Convert JSON dataset to pandas Data Frame

pd_data_frame = pd.DataFrame(convert_json_to_data_frame("assets/nuscene_US_rainy_clear_engg_embedding.json", "field_data")).to_pickle('field-data-nuscene_US_rainy_clear_engg_embedding.pkl')

# # data_frame_extractor(pd_data_frame).to_csv("TestingDataFrame.csv", index=False)
dataset_ = "field"
version = "v1"
pd_data_frame = pd.read_pickle(f"{dataset_}-data-nuscene_US_rainy_clear_engg_embedding.pkl")

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("location", AttributeSchemaElement(), pd_data_frame)
schema.add("vehicle_no", AttributeSchemaElement(), pd_data_frame)
schema.add("date_captured", AttributeSchemaElement(), pd_data_frame)
schema.add("channel", AttributeSchemaElement(), pd_data_frame)
schema.add("dataset_type", AttributeSchemaElement(), pd_data_frame)
schema.add("ImageEmbedding", ImageEmbeddingSchemaElement(model="imageModel"), pd_data_frame)

#create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject",run_name= f"{dataset_}-run-21-aug-{version}")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name=f"{dataset_}-dataset-21-aug-{version}")

#load schema and pandas data frame
test_ds.load(data=pd_data_frame, schema=schema)