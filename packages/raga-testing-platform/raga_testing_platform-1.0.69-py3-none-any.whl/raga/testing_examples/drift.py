from raga import *

project_name = "testingProject"
run_name = "drift-7-aug-v4"

test_session = TestSession(project_name="testingProject",
                           run_name="drift-7-aug-v4",
                           u_test=True)
test_session.token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbkByYWdhIiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJ1c2VyTmFtZSI6ImFkbWluQHJhZ2EiLCJleHAiOjE2OTE1NTgwNTYsImlhdCI6MTY5MTQ3MTY1Niwib3JnSWQiOjEsImp0aSI6ImFkbWluQHJhZ2EifQ.jhDiidIdA2AFuNgWuFAwM2iTdXZHb7wvlaaM-nptakni6QvGh0QscFj-3tKTvEna1hqjNyx0mo9lhpnFtxgqOg"
test_session.project_id = 1
test_session.experiment_id = 1701

rules = DriftDetectionRules()
rules.add(type="anomaly_detection", dist_metric="Euclidian", _class="All", threshold=0.6)

edge_case_detection = data_drift_detection(test_session=test_session,
                                           test_name="dift-8-aug-v2",
                                           train_dataset_name="train-dataset-7-aug-v2",
                                           field_dataset_name="field-dataset-7-aug-v2",
                                           train_embed_col_name="ImageEmbedding",
                                           field_embed_col_name = "ImageEmbedding" ,
                                           level = "image",
                                           aggregation_level=["location", "vehicle_no", "date_captured", "channel", "dataset_type"],
                                           rules = rules)


test_session.add(edge_case_detection)

test_session.run()