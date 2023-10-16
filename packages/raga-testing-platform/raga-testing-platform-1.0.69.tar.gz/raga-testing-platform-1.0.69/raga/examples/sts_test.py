from raga import *
import pandas as pd
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def image_id(row):
    file = row["SourceLink"].split("/")[-1]
    return StringElement(file)

def csv_parser(csv_file):
    df = pd.read_csv(csv_file)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df.apply(image_id , axis=1)
    data_frame["ImageUri"] = df["SourceLink"].apply(lambda x: StringElement(f"https://product-uploads-raga.s3.ap-south-1.amazonaws.com/data/{x.split('/')[-1]}"))
    return data_frame.head(100)

###################################################################################################
pd_data_frame = csv_parser("./assets/labelling_qc_score_df-copy.csv")


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())

run_name = f"Pre-UAT-DS-29sep-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/raga-importer")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session,
                  name="Pre-UAT-DS-29sep-v3",
                  type=DATASET_TYPE.IMAGE,
                  data=pd_data_frame, 
                  schema=schema, 
                  creds=cred)

#load to server
test_ds.load()