from raga import *
import datetime

run_name = f"run-labeling-quality-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
# test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="qGIXoxPVMObBs9DzBXuX", secret_key="VqpODChJcTi3QHWmr4PZiX6D1aXxid7QSd7YKpyJ", host="http://prod-raga.ragaai.in")

rules = LQRules()
rules.add(metric="mistake_score", label=["ALL"], metric_threshold=0.005)


edge_case_detection = labelling_quality_test(test_session=test_session,
                                            dataset_name = "100-sport-dataset-100-v2",
                                            test_name = "Labeling Quality Test",
                                            type = "labelling_consistency",
                                            output_type="image_classification",
                                            mistake_score_col_name = "MistakeScore",
                                            embedding_col_name = "ImageVectorsM1",
                                            rules = rules)
test_session.add(edge_case_detection)

test_session.run()