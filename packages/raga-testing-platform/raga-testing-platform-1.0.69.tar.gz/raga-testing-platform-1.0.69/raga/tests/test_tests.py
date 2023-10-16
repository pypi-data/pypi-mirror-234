import unittest
from raga import Dataset, StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement
from raga import model_ab_test, ab_test_validation, TestSession, FloatElement
from unittest import mock
from unittest.mock import MagicMock, patch, Mock, call

class TestABTestTestCase(unittest.TestCase):
    def setUp(self):
        self.test_session = TestSession("project_name", "run_name", u_test=True)
        self.test_session.project_id = "project_id"
        self.test_session.token = "test_token"
        self.test_session.api_host = "base_url"
        self.dataset_name = "my_dataset"
        self.test_session.experiment_id = "experiment_id"
        self.dataset_creds = None
        self.test_ds = Dataset(self.test_session, self.dataset_name, self.dataset_creds, u_test=True)
        self.test_ds.dataset_id = "12345"


        self.testName = StringElement("TestName")
        self.modelA = StringElement("modelA")
        self.modelB = StringElement("modelB")
        self.gt = StringElement("GT")
        self.type = ModelABTestTypeElement("unlabelled")
        self.filter = StringElement("unlabelled")
        self.aggregation_level = AggregationLevelElement()
        self.aggregation_level.add(StringElement("weather"))
        self.aggregation_level.add(StringElement("scene"))
        self.aggregation_level.add(StringElement("time_of_day"))
        self.rules = ModelABTestRules()
        self.rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        self.rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

    def test_ab_test_validation(self):
        # Test valid inputs
        self.assertTrue(ab_test_validation(self.test_ds, self.testName, self.modelA, self.modelB,
                                            self.type, self.aggregation_level, self.rules))

        # Test invalid test_ds
        with self.assertRaises(AssertionError):
            ab_test_validation("invalid_test_ds", self.testName, self.modelA, self.modelB,
                                self.type, self.aggregation_level, self.rules)

        # Test missing testName
        with self.assertRaises(AssertionError):
            ab_test_validation(self.test_ds, None, self.modelA, self.modelB,
                                self.type, self.aggregation_level, self.rules)

        # Test missing modelA
        with self.assertRaises(AssertionError):
            ab_test_validation(self.test_ds, self.testName, None, self.modelB,
                                self.type, self.aggregation_level, self.rules)

        # Test missing modelB
        with self.assertRaises(AssertionError):
            ab_test_validation(self.test_ds, self.testName, self.modelA, None,
                                self.type, self.aggregation_level, self.rules)
            
        # Test missing type
        with self.assertRaises(AssertionError):
            ab_test_validation(self.test_ds, self.testName, self.modelA, self.modelB,
                                None, self.aggregation_level, self.rules)
            
        # Test missing aggregation_level
        with self.assertRaises(AssertionError):
            ab_test_validation(self.test_ds, self.testName, self.modelA, self.modelB,
                                self.type, None, self.rules)
            
        # Test missing rules
        with self.assertRaises(AssertionError):
            ab_test_validation(self.test_ds, self.testName, self.modelA, self.modelB,
                                self.type, self.aggregation_level, None)
        
        # Test type labelled
        self.type = ModelABTestTypeElement("labelled")
        self.gt = StringElement("")
        with self.assertRaises(AssertionError):
            ab_test_validation(test_ds=self.test_ds, testName=self.testName, modelA=self.modelA, modelB=self.modelB,
                                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules, gt=self.gt)

         # Test type unlabelled
        self.type = ModelABTestTypeElement("unlabelled")
        self.gt = StringElement("GT")
        with self.assertRaises(ValueError):
            ab_test_validation(test_ds=self.test_ds, testName=self.testName, modelA=self.modelA, modelB=self.modelB,
                                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules, gt=self.gt)

    def test_model_ab_test_labelled(self):
        # Test valid inputs
        self.type = ModelABTestTypeElement("labelled")
        self.gt = StringElement("GT")
        result = model_ab_test(test_ds=self.test_ds, testName=self.testName, modelA=self.modelA, modelB=self.modelB,
                                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules, filter=self.filter, gt=self.gt)
        self.assertEqual(result["datasetId"], self.test_ds.dataset_id)
        self.assertEqual(result["experimentId"], self.test_ds.test_session.experiment_id)
        self.assertEqual(result["name"], self.testName.get())
        self.assertEqual(result["filter"], self.filter.get())
        self.assertEqual(result["modelA"], self.modelA.get())
        self.assertEqual(result["modelB"], self.modelB.get())
        self.assertEqual(result["type"], self.type.get())
        self.assertEqual(result["aggregationLevels"], self.aggregation_level.get())
        self.assertEqual(result["rules"], self.rules.get())
        self.assertEqual(result["gt"], self.gt.get())
        
        with unittest.mock.patch("raga._tests.ab_test_validation") as mock_validation:
            model_ab_test(test_ds=self.test_ds, testName=self.testName, modelA=self.modelA, modelB=self.modelB,
                                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules, gt= self.gt)
            mock_validation.assert_called_with(self.test_ds,self.testName, self.modelA, self.modelB, self.type, self.aggregation_level, self.rules, self.gt)

    def test_model_ab_test_unlabelled(self):
        # Test valid inputs
        self.type = ModelABTestTypeElement("unlabelled")
        result = model_ab_test(test_ds=self.test_ds, testName=self.testName, modelA=self.modelA, modelB=self.modelB,
                                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules, filter=self.filter)
        self.assertEqual(result["datasetId"], self.test_ds.dataset_id)
        self.assertEqual(result["experimentId"], self.test_ds.test_session.experiment_id)
        self.assertEqual(result["name"], self.testName.get())
        self.assertEqual(result["filter"], self.filter.get())
        self.assertEqual(result["modelA"], self.modelA.get())
        self.assertEqual(result["modelB"], self.modelB.get())
        self.assertEqual(result["type"], self.type.get())
        self.assertEqual(result["aggregationLevels"], self.aggregation_level.get())
        self.assertEqual(result["rules"], self.rules.get())

        with unittest.mock.patch("raga._tests.ab_test_validation") as mock_validation:
            model_ab_test(test_ds=self.test_ds, testName=self.testName, modelA=self.modelA, modelB=self.modelB,
                                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules, gt= self.gt)
            mock_validation.assert_called_with(self.test_ds,self.testName, self.modelA, self.modelB, self.type, self.aggregation_level, self.rules, self.gt)
        


if __name__ == '__main__':
    unittest.main()