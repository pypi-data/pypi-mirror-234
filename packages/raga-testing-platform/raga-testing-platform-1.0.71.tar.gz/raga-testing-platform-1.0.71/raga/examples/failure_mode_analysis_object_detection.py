
import datetime
from raga.raga_schema import FMARules
from raga._tests import clustering, failure_mode_analysis
from raga.test_session import TestSession


run_name = f"run-failure-mode-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

rules = FMARules()
rules.add(metric="Precision", conf_threshold=0.8, metric_threshold=0.5, iou_threshold=0.5, overlap_threshold=0.5, label="ALL")

cls_default = clustering(method="k-means", embedding_col="ImageVectorsM1", level="image", args= {"numOfClusters": 5}, interpolation=True)

# edge_case_detection = failure_mode_analysis(test_session=test_session,
#                                             dataset_name = "lm-hb-video-ds-v7",
#                                             test_name = "FMA OD Video Test",
#                                             model = "modelA",
#                                             gt = "modelB",
#                                             rules = rules,
#                                             output_type="object_detection",
#                                             type="embedding",
#                                             clustering=cls_default
#                                             )

# edge_case_detection = failure_mode_analysis(test_session=test_session,
#                                             dataset_name = "lm-hb-video-ds-v7",
#                                             test_name = "FMA OD Video Test",
#                                             model = "modelA",
#                                             gt = "modelB",
#                                             rules = rules,
#                                             output_type="object_detection",
#                                             type="metadata",
#                                             aggregation_level=["weather", "scene"]
#                                             )

edge_case_detection = failure_mode_analysis(test_session=test_session,
                                            dataset_name = "stopsign-event-video-ds-full-v3",
                                            test_name = "FMA OD Video Event Test",
                                            model = "Production-America-Stop-Event",
                                            gt = "Complex-America-Stop-Event",
                                            object_detection_model="Complex-America-Stop-Model",
                                            object_detection_gt = "Production-America-Stop-Model",
                                            rules = rules,
                                            output_type="event_detection",
                                            type="metadata",
                                            aggregation_level=["weather", "scene"]
                                            )


test_session.add(edge_case_detection)

test_session.run()