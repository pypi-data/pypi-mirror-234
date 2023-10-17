from raga import *
import datetime

run_name = f"run-labeling-quality-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

rules = LQRules()
rules.add(metric="mistake_score", label=["ALL"], metric_threshold=0.0012)


edge_case_detection = labelling_quality_test(test_session=test_session,
                                            dataset_name = "satsure-area-dataset-v1",
                                            test_name = "Labeling Quality Test",
                                            type = "labelling_consistency",
                                            output_type="semantic_segmentation",
                                            mistake_score_col_name = "MistakeScores",
                                            rules = rules)
test_session.add(edge_case_detection)

test_session.run()