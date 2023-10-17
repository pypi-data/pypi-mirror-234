import pathlib
import random
from raga import *
import pandas as pd
import datetime
import numpy as np

weather_data = {
    "overcast": "overcast",
    "fog": "fog",
    "cloudy": "overcast",
    "sunny": "clear",
    "clear": "clear",
    "snow": "snow",
    "rain": "rain",
    "partly cloudy": "overcast",
    "light rain": "rain",
    "patchy light rain with thunder": "rain",
    "patchy light rain": "rain",
    "light drizzle": "rain",
    "light freezing rain": "rain",
    "thundery outbreaks possible": "overcast",
    "patchy rain possible": "overcast",
    "patchy light drizzle": "rain",
    "heavy freezing drizzle":"rain",
    "moderate snow": "snow",
    "moderate rain at times": "rain",
    "moderate rain": "rain",
    "moderate or heavy snow showers": "snow",
    "moderate or heavy rain shower": "rain",
    "moderate or heavy rain with thunder":"rain",
    "moderate or heavy freezing rain":"rain",
    "heavy rain":"rain",
    "heavy snow":"snow",
    "mist": "fog",
    "freezing fog":"fog",
    "light snow": "snow",
    "light snow showers": "snow",
    "light sleet showers": "snow",
    "light sleet": "snow",
    "light rain shower": "rain",
    "blowing snow": "snow",
    "patchy light snow":"snow",
    "patchy moderate snow":"snow",
    "ice pellets":"snow",
    "blizzard":"blizzard",
    "":""
}


def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    return StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/StopSign_Part1_event.json/data_points/{pathlib.Path(x).stem}/{x}")

def model_a_inference(row):
    detections = EventDetectionObject()
    start_frame = row["model_1_outputs"][0]["frame_id"]
    end_frame = row["model_1_outputs"][-1]["frame_id"]
    for index, frame in enumerate(row["outputs"]):
        for detection in frame["detections"]:
            for ind, count in enumerate(range(int(detection["count"]))):
                id = ind+1
                detections.add(EventDetection(Id=id, StartFrame=start_frame, EndFrame=end_frame, EventType=detection["class"], Confidence=detection["confidence"]))
    return detections


def model_b_inference(row):
    detections = EventDetectionObject()
    start_frame = row["model_1_outputs"][0]["frame_id"]
    end_frame = row["model_1_outputs"][-1]["frame_id"]
    for index, frame in enumerate(row["outputs"]):
        for detection in frame["detections"]:
            for ind, count in enumerate(range(int(detection["count"]))):
                id = ind+1
                detections.add(EventDetection(Id=id, StartFrame=start_frame, EndFrame=end_frame, EventType=detection["class"], Confidence=detection["confidence"]))
    return detections

def model_a_video_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["model_1_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=float(frame["time_offset_ms"])*1000, detections=detections))

    return model_a_inference


def model_b_video_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["model_2_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=float(frame["time_offset_ms"])*1000, detections=detections))

    return model_a_inference


def model_image_inference(row):
    AnnotationsV1 = ImageDetectionObject()
    for index, detection in enumerate(row["detections"]):
        AnnotationsV1.add(ObjectDetection(Id=detection["Id"], ClassId=0, ClassName=detection['ClassName'], Confidence=detection['Confidence'], BBox= detection['BBox'], Format=detection['Format']))
    return AnnotationsV1

def generate_random_list():
    """
    Generate a random list of specified length containing floating-point numbers.

    Args:
        length (int): The number of elements in the list.

    Returns:
        A list of random floating-point numbers.
    """
    list_data = [random.choice([random.uniform(1, 20), random.uniform(1, 20), random.uniform(-10, 20)]), random.choice([random.uniform(1, 20), random.uniform(1, 20), random.uniform(-10, 20)]), random.choice([random.uniform(1, 20), random.uniform(1, 20), random.uniform(-10, 20)])]
    embeddings = ImageEmbedding()
    for embedding in list_data:
        # print(embedding)
        embeddings.add(Embedding(int(embedding)))
    return embeddings


def json_parser(event_1, event_2, model_1, model_2):
    event_1_df = pd.read_json(event_1)
    event_2_df = pd.read_json(event_2)
    model_1_df = pd.read_json(model_1)
    model_2_df = pd.read_json(model_2)
    event_1_df_exploded = event_1_df.explode('inputs')
    event_2_df_exploded = event_2_df.explode('inputs')
    model_1_df_exploded = model_1_df.explode('inputs')
    model_2_df_exploded = model_2_df.explode('inputs')
    attributes = event_2_df["attributes"].apply(pd.Series)
    event_2_df_exploded = pd.concat([event_2_df_exploded, attributes], axis=1)
    event_2_df_exploded.rename(columns={"outputs": "new_outputs"}, inplace=True)
    model_1_df_exploded.rename(columns={"outputs": "model_1_outputs"}, inplace=True)
    model_2_df_exploded.rename(columns={"outputs": "model_2_outputs"}, inplace=True)
    merged_df = pd.merge(event_1_df_exploded, event_2_df_exploded, on='inputs')
    merged_df = pd.merge(merged_df, model_1_df_exploded, on='inputs')
    merged_df = pd.merge(merged_df, model_2_df_exploded, on='inputs', suffixes=[None, "_model_2"])
    data_frame = pd.DataFrame()
    data_frame["videoId"] = merged_df["inputs"].apply(lambda x: StringElement(pathlib.Path(x).stem))
    data_frame["videoUrl"] = merged_df["inputs"].apply(lambda x: img_url(x))
    data_frame["timeOfCapture"] = merged_df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["sourceLink"] = merged_df["inputs"].apply(lambda x: StringElement(x))
    data_frame["dutyType"] = merged_df["dutyType"].apply(lambda x: StringElement(x))
    data_frame["time_of_day"] = merged_df["time_of_day"].apply(lambda x: StringElement(x))
    data_frame["weather"] = merged_df["weather"].apply(lambda x: StringElement(x))
    data_frame["scene"] = merged_df["scene"].apply(lambda x: StringElement(x))
    data_frame["tags"] = merged_df["tags"].apply(lambda x: StringElement(x))
    data_frame["Complex-America-Stop-Event"] = merged_df.apply(model_a_inference, axis=1)
    data_frame["Production-America-Stop-Event"] = merged_df.apply(model_b_inference, axis=1)
    data_frame["Complex-America-Stop-Model"] = merged_df.apply(model_a_video_inference, axis=1)
    data_frame["Production-America-Stop-Model"] = merged_df.apply(model_b_video_inference, axis=1)
    return data_frame

def make_image_df(video_df:pd.DataFrame):
    df = data_frame_extractor(video_df)
    videos = df["videoId"]
    complex_model = df['Complex-America-Stop-Model']
    production_model = df['Production-America-Stop-Model']
    data_frame_list = []
    for index, output in enumerate(complex_model):
        frames  = output['frames']
        video = videos[index]
        complex_model_outputs = complex_model[index]['frames']
        production_model_outputs = production_model[index]['frames']
        for frame_index, frame in enumerate(frames):
            complex_detection = complex_model_outputs[frame_index]
            production_detection = production_model_outputs[frame_index]
            data_frame_list.append({
                "imageId":StringElement(f"img_{video}_{str(frame.get('frameId')).zfill(8)}"),
                "frame":StringElement(frame.get('frameId')),
                "videoId":StringElement(video),
                "imageUrl":StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/StopSign_Part1_event.json/data_points/{video}/images/img_{video}_{str(frame.get('frameId')).zfill(8)}.jpg"),
                "timeOfCapture":TimeStampElement(get_timestamp_x_hours_ago(frame.get('frameId'))),
                "sourceLink":StringElement(f"img_{video}_{str(frame.get('frameId')).zfill(8)}"),
                "dutyType":StringElement(df["dutyType"][index]),
                "time_of_day":StringElement(df["time_of_day"][index]),
                "weather":StringElement(weather_data[str(df["weather"][index]).lower()]),
                "scene":StringElement(df["scene"][index]),
                "tags":StringElement(df["tags"][index]),
                "Complex-America-Stop-Model": model_image_inference(complex_detection),
                "Production-America-Stop-Model": model_image_inference(production_detection)
            })

    return pd.DataFrame(data_frame_list)

# pd_video_data_frame = json_parser("./assets/Complex-America-Stop-Event.json", "./assets/Production-America-Stop-Event.json", "./assets/Complex-America-Stop-Model.json", "./assets/Production-America-Stop-Model.json")
# # # data_frame_extractor(pd_video_data_frame).to_csv("assets/event_ds_10.csv", index=False)

# pd_image_data_frame = make_image_df(pd_video_data_frame)

# # # # data_frame_extractor(pd_image_data_frame).to_csv("assets/event_ds_pd_image_data_frame_1.csv", index=False)

# # # run_name = f"lm_video_loader_failure_mode_analysis_object_detection-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


# def count_rows_and_chunk(df, chunk_size):
#     """
#     Count the rows of a Pandas DataFrame and break it into smaller chunks.

#     Parameters:
#         df (pd.DataFrame): The input Pandas DataFrame.
#         chunk_size (int): The size of each chunk.

#     Returns:
#         (int, list of pd.DataFrame): A tuple containing the total row count of the DataFrame
#                                      and a list of DataFrame chunks.
#     """
#     total_rows = len(df)
#     num_chunks = (total_rows + chunk_size - 1) // chunk_size  # Calculate the number of chunks needed
#     chunks = [df[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
#     return total_rows, chunks


# chunk_size = 30000  # Maximum chunk size

# total_rows, chunks = count_rows_and_chunk(pd_image_data_frame, chunk_size)
# print(f"Total Rows: {total_rows}")
# for i, chunk in enumerate(chunks):
#    chunk.to_pickle(f"./assets/Complex-production-America-Stop-Sign/ss_data_{str(i).zfill(8)}.pkl")



# image_ds_schema = RagaSchema()
# image_ds_schema.add("imageId", PredictionSchemaElement())
# image_ds_schema.add("frame", FrameSchemaElement())
# image_ds_schema.add("videoId", ParentSchemaElement())
# image_ds_schema.add("imageUrl", ImageUriSchemaElement())
# image_ds_schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
# image_ds_schema.add("sourceLink", FeatureSchemaElement())
# image_ds_schema.add("weather", AttributeSchemaElement())
# image_ds_schema.add("time_of_day", AttributeSchemaElement())
# image_ds_schema.add("scene", AttributeSchemaElement())
# image_ds_schema.add("Complex-America-Stop-Model", InferenceSchemaElement(model="Complex-America-Stop-Event"))
# image_ds_schema.add("Production-America-Stop-Model", InferenceSchemaElement(model="Production-America-Stop-Event"))


# create test_session object of TestSession instance
# test_session = TestSession(project_name="testingProject", run_name= run_name)

# creds = DatasetCreds(arn="arn:aws:iam::527593518644:role/raga-importer")
#create test_ds object of Dataset instance
# image_ds = Dataset(test_session=test_session,
#                   name="stopsign-event-image-ds-v8",
#                   type=DATASET_TYPE.IMAGE,
#                   data=pd_image_data_frame,
#                   schema=image_ds_schema,
#                   creds=creds)

# #load schema and pandas data frame
# image_ds.load()

# model_exe_fun = ModelExecutorFactory().get_model_executor(test_session=test_session, 
#                                                           model_name="Lightmetrics Model", 
#                                                           version="0.1.1")

# model_exe_fun.execute(init_args={"device": "cpu", "frame_sampling_rate":30}, 
#                            execution_args={"input_columns":{"img_paths":"imageUrl"}, 
#                                            "output_columns":{"embedding":"imageEmbedding"},
#                                            "column_schemas":{"embedding":ImageEmbeddingSchemaElement(model="Lightmetrics Model")}}, 
#                            data_frame=image_ds)

# image_ds.load()


# video_schema = RagaSchema()
# video_schema.add("videoId", PredictionSchemaElement())
# video_schema.add("videoUrl", ImageUriSchemaElement())
# video_schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
# video_schema.add("sourceLink", FeatureSchemaElement())
# video_schema.add("dutyType", AttributeSchemaElement())
# video_schema.add("time_of_day", AttributeSchemaElement())
# video_schema.add("weather", AttributeSchemaElement())
# video_schema.add("scene", AttributeSchemaElement())
# video_schema.add("tags", AttributeSchemaElement())
# video_schema.add("Complex-America-Stop-Event", EventInferenceSchemaElement(model="Complex-America-Stop-Event"))
# video_schema.add("Production-America-Stop-Event", EventInferenceSchemaElement(model="Production-America-Stop-Event"))

# #create test_ds object of Dataset instance
# video_ds = Dataset(test_session=test_session,
#                   name="stopsign-event-video-ds-full-v1",
#                   type=DATASET_TYPE.VIDEO,
#                   data=pd_video_data_frame,
#                   schema=video_schema,
#                   creds=creds,
#                   parent_dataset="stopsign-event-img-ds-full-v1")
# #load schema and pandas data frame
# video_ds.load()

run_name = f"lm_video_loader_failure_mode_analysis_object_detection-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
test_session = TestSession(project_name="testingProject", run_name= run_name)


paths = []
folder_path = "./assets/Complex-production-America-Stop-Sign-1"
# Check if the folder path exists
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Get a list of all files in the folder
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Print the list of files with their full paths
    for file_name in file_list:
        full_path = os.path.join(folder_path, file_name)
        paths.append(full_path)
else:
    print(f"The folder path '{folder_path}' does not exist or is not a directory.")
paths = sorted(paths)
# print(paths)
for path in paths:
    image_ds_schema = RagaSchema()
    image_ds_schema.add("imageId", PredictionSchemaElement())
    image_ds_schema.add("frame", FrameSchemaElement())
    image_ds_schema.add("videoId", ParentSchemaElement())
    image_ds_schema.add("imageUrl", ImageUriSchemaElement())
    image_ds_schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
    image_ds_schema.add("sourceLink", FeatureSchemaElement())
    image_ds_schema.add("weather", AttributeSchemaElement())
    image_ds_schema.add("time_of_day", AttributeSchemaElement())
    image_ds_schema.add("scene", AttributeSchemaElement())
    image_ds_schema.add("Complex-America-Stop-Model", InferenceSchemaElement(model="Complex-America-Stop-Event"))
    image_ds_schema.add("Production-America-Stop-Model", InferenceSchemaElement(model="Production-America-Stop-Event"))

    creds = DatasetCreds(arn="arn:aws:iam::527593518644:role/model-distribution")
    # create test_ds object of Dataset instance
    df = pd.read_pickle(path)
    print("PAAAAAATH", path)
    test_ds = Dataset(test_session=test_session, 
                      name="stopsign-event-img-ds-full-v3", 
                      type=DATASET_TYPE.IMAGE,
                      data=df, 
                      schema=image_ds_schema, 
                      creds=creds)

    #load schema and pandas data frame
    test_ds.load()

    model_exe_fun = ModelExecutorFactory().get_model_executor(test_session=test_session, 
                                                          model_name="Lightmetrics Embedding Model", 
                                                          version="0.1.2")

    df = model_exe_fun.execute(init_args={"device": "cpu", "frame_sampling_rate":30}, 
                            execution_args={"input_columns":{"img_paths":"imageUrl"}, 
                                            "output_columns":{"embedding":"imageEmbedding"},
                                            "column_schemas":{"embedding":ImageEmbeddingSchemaElement(model="Lightmetrics Embedding Model")}}, 
                            data_frame=test_ds)

    print(df)
    test_ds.load()