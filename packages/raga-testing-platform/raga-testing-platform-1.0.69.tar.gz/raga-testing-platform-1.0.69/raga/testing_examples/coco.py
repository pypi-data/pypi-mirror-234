# from raga import *
# import pandas as pd


# project_name = "testingProject" # Project Name
# run_name= "K_COCO_19Jul_V2_v9" # Experiment Name
# dataset_name = "k_coco_Ds_19jul_V2_v1" # Dataset Name


# #create test_session object of TestSession instance
# test_session = TestSession(project_name=project_name,run_name=run_name)

# #create test_ds object of Dataset instance
# test_ds = Dataset(test_session=test_session, name=dataset_name)

# #load schema and pandas data frame
# test_ds.load(data="macoco.json", format="coco", model_name="modelA", inference_col_name="annotations1")
# test_ds.load(data="mbcoco.json", format="coco", model_name="modelB", inference_col_name="annotations2")
# test_ds.load(data="gtcoco.json", format="coco", model_name="modelG", inference_col_name="annotations3")

# # Params for labelled AB Model Testing
# testName = StringElement("TestingP-unlabelled-test-1")
# modelA = StringElement("modelA")
# modelB = StringElement("modelB")
# gt = StringElement("modelG")
# type = ModelABTestTypeElement("labelled")
# rules = ModelABTestRules()
# rules.add(metric = StringElement("precision_diff_all"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("precision_candy"), IoU = FloatElement(0.5), _class = StringElement("candy"), threshold = FloatElement(0.5))
# #create payload for model ab testing
# model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, testName=testName, modelA = modelA , modelB = modelB , type = type, rules = rules, gt=gt)

# #add payload into test_session object
# test_session.add(model_comparison_check)

# #run added ab test model payload
# test_session.run()

# # Params for unlabelled AB Model Testing
# testName = StringElement("19July_TestCOCO_KB_01")
# modelA = StringElement("modelA")
# modelB = StringElement("modelB")
# type = ModelABTestTypeElement("unlabelled")
# rules = ModelABTestRules()
# rules.add(metric = StringElement("difference_all"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("difference_candy"), IoU = FloatElement(0.5), _class = StringElement("candy"), threshold = FloatElement(0.5))
# rules.add(metric = StringElement("difference_drink"), IoU = FloatElement(0.5), _class = StringElement("drink"), threshold = FloatElement(0.5))

# #create payload for model ab testing
# model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, testName=testName, modelA = modelA , modelB = modelB , type = type, rules = rules)

# #add payload into test_session object
# test_session.add(model_comparison_check)

# #run added ab test model payload
# test_session.run()