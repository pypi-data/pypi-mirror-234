from raga import *


test_session = TestSession(project_name="LivenessDetection",
                           run_name="clustering-25-aug-v1")

rules = FMARules()
rules.add(metric="Precision", conf_threshold=0.8, metric_threshold=0.5, label="ALL")

cls_default = clustering(method="k-means", embedding_col="ImageVectorsM1", level="image", args= {"numOfClusters": 5})

edge_case_detection = failure_mode_analysis(test_session=test_session,
                                            dataset_name = "spoof-dataset",
                                            test_name = "Test",
                                            model = "modelB",
                                            gt = "GT",
                                            clustering = cls_default,
                                            rules = rules,
                                            output_type="multi-label")

test_session.add(edge_case_detection)

test_session.run()