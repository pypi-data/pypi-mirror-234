from typing import Optional
from raga import TestSession, ModelABTestRules, FMARules, LQRules

def model_ab_test(test_session:TestSession, 
                  dataset_name: str, 
                  test_name: str, 
                  modelA: str, 
                  modelB: str,
                  type: str, 
                  rules: ModelABTestRules, 
                  aggregation_level:  Optional[list] = [],
                  gt: Optional[str] = "", 
                  filter: Optional[str] = ""):
    dataset_id = ab_test_validation(test_session, dataset_name, test_name, modelA, modelB, type, rules, gt, aggregation_level)    
    return {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": test_name,
            "modelA": modelA,
            "modelB": modelB,
            "type": type,
            "rules": rules.get(),
            "aggregationLevels": aggregation_level,
            'filter':filter,
            'gt':gt,
            'test_type':'ab_test'
        }

def ab_test_validation(test_session:TestSession, 
                       dataset_name: str, 
                       test_name: str, 
                       modelA: str, 
                       modelB: str,
                       type: str, 
                       rules: ModelABTestRules,
                       gt: Optional[str] = "", 
                       aggregation_level:Optional[list] = []):
    from raga.constants import INVALID_RESPONSE, INVALID_RESPONSE_DATA, REQUIRED_ARG_V2

    assert isinstance(test_session, TestSession), f"{REQUIRED_ARG_V2.format('test_session', 'instance of the TestSession')}"
    assert isinstance(dataset_name, str) and dataset_name, f"{REQUIRED_ARG_V2.format('dataset_name', 'str')}"

    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})

    if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)
    
    dataset_id = res_data.get("data", {}).get("id")

    if not dataset_id:
        raise KeyError(INVALID_RESPONSE_DATA)
    
    assert isinstance(test_name, str) and test_name, f"{REQUIRED_ARG_V2.format('test_name', 'str')}"
    assert isinstance(modelA, str) and modelA, f"{REQUIRED_ARG_V2.format('modelA', 'str')}"
    assert isinstance(modelB, str) and modelB, f"{REQUIRED_ARG_V2.format('modelB', 'str')}"
    assert isinstance(type, str), f"{REQUIRED_ARG_V2.format('type', 'str')}"
    assert isinstance(rules, ModelABTestRules) and rules.get(), f"{REQUIRED_ARG_V2.format('rules', 'instance of the ModelABTestRules')}"

    if aggregation_level:
        assert isinstance(aggregation_level, list), f"{REQUIRED_ARG_V2.format('aggregation_level', 'str')}"

    if type == "labelled":
        assert isinstance(gt, str) and gt, f"{REQUIRED_ARG_V2.format('gt', 'str')}"

    if type == "unlabelled" and isinstance(gt, str) and gt:
        raise ValueError("gt is not required on unlabelled type.")
    
    return dataset_id

def failure_mode_analysis(test_session:TestSession, 
                          dataset_name:str, 
                          test_name:str, 
                          model:str, 
                          gt:str,
                          rules:FMARules, 
                          output_type:str, 
                          type:str, 
                          clustering:Optional[dict]={}, 
                          aggregation_level:Optional[list]=[],
                          object_detection_model:Optional[str]="",
                          object_detection_gt:Optional[str]=""
                          ):
    
    dataset_id = failure_mode_analysis_validation(test_session=test_session, dataset_name=dataset_name, test_name=test_name, model=model, gt=gt, type=type, rules=rules, output_type=output_type, aggregation_level=aggregation_level, clustering=clustering)
   
    response = {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": test_name,
            "model": model,
            "gt": gt,
            "type": type,
            "rules": rules.get(),
            "test_type":"cluster",
            "filter":"",
            "outputType":output_type,
            "aggregationLevels":aggregation_level,
        }
    if output_type == "event_detection":
         response['objectDetectionModel'] = object_detection_model
         response['objectDetectionGT'] = object_detection_gt
    if clustering:
         response['clustering'] = clustering
    return response

def failure_mode_analysis_validation(test_session:TestSession, dataset_name:str, test_name:str, model:str, gt:str, rules:FMARules, output_type:str, type:str, aggregation_level:Optional[list]=[], clustering:Optional[dict]=None):
    from raga.constants import INVALID_RESPONSE, INVALID_RESPONSE_DATA, REQUIRED_ARG_V2

    assert isinstance(test_session, TestSession), f"{REQUIRED_ARG_V2.format('test_session', 'instance of the TestSession')}"
    assert isinstance(dataset_name, str) and dataset_name, f"{REQUIRED_ARG_V2.format('dataset_name', 'str')}"
    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})

    if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)
    
    dataset_id = res_data.get("data", {}).get("id")

    if not dataset_id:
        raise KeyError(INVALID_RESPONSE_DATA)
    assert isinstance(test_name, str) and test_name, f"{REQUIRED_ARG_V2.format('test_name', 'str')}"
    assert isinstance(model, str) and model, f"{REQUIRED_ARG_V2.format('model', 'str')}"
    assert isinstance(gt, str) and gt, f"{REQUIRED_ARG_V2.format('gt', 'str')}"
    assert isinstance(type, str) and type, f"{REQUIRED_ARG_V2.format('type', 'str')}"
    assert isinstance(rules, FMARules) and rules, f"{REQUIRED_ARG_V2.format('rules', 'instance of the FMARules')}"
    assert isinstance(output_type, str) and output_type, f"{REQUIRED_ARG_V2.format('output_type', 'str')}"

    if output_type == "object_detection":
         if type == "embedding" and not clustering:
              raise ValueError(f"{REQUIRED_ARG_V2.format('clustering', 'clustering function')}")
         if type == "metadata":
            assert isinstance(aggregation_level, list) and aggregation_level, f"{REQUIRED_ARG_V2.format('aggregation_level', 'list')}"
    return dataset_id

def clustering(method:str, embedding_col:str, level:str, args=dict, interpolation:bool=False):
    from raga.constants import REQUIRED_ARG_V2

    assert isinstance(method, str) and method, f"{REQUIRED_ARG_V2.format('method', 'str')}"
    assert isinstance(embedding_col, str) and embedding_col, f"{REQUIRED_ARG_V2.format('embedding_col', 'str')}"
    assert isinstance(level, str) and level, f"{REQUIRED_ARG_V2.format('level', 'str')}"
    return {
        "method":method,
        "embeddingCol":embedding_col,
        "level":level,
        "args":args,
        "interpolation":interpolation
    } 


def labelling_quality_test(test_session:TestSession, 
                           dataset_name:str, 
                           test_name:str, 
                           type:str, 
                           output_type: str, 
                           rules:LQRules, 
                           mistake_score_col_name: str,
                           embedding_col_name:Optional[str]=""):
    
    dataset_id = labelling_quality_test_validation(test_session, dataset_name, test_name, type, output_type, rules, mistake_score_col_name)
    return {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": test_name,
            "type": type,
            "outputType": output_type,
            "rules": rules.get(),
            "mistakeScoreColName":mistake_score_col_name,
            "embeddingColName":embedding_col_name,
            "test_type":"labelling_quality",
            "filter":"",
        }


def labelling_quality_test_validation(test_session:TestSession, dataset_name:str, test_name:str, type:str, output_type:str,  rules:LQRules, mistake_score_col_name:str):
    from raga.constants import INVALID_RESPONSE, INVALID_RESPONSE_DATA, REQUIRED_ARG_V2

    assert isinstance(test_session, TestSession), f"{REQUIRED_ARG_V2.format('test_session', 'instance of the TestSession')}"
    assert isinstance(dataset_name, str) and dataset_name, f"{REQUIRED_ARG_V2.format('dataset_name', 'str')}"
    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})

    if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)
    dataset_id = res_data.get("data", {}).get("id")

    if not dataset_id:
        raise KeyError(INVALID_RESPONSE_DATA)
    
    assert isinstance(test_name, str) and test_name, f"{REQUIRED_ARG_V2.format('test_name', 'str')}"
    assert isinstance(type, str) and type, f"{REQUIRED_ARG_V2.format('type', 'str')}"
    assert isinstance(output_type, str) and output_type, f"{REQUIRED_ARG_V2.format('output_type', 'str')}"
    assert isinstance(mistake_score_col_name, str) and mistake_score_col_name, f"{REQUIRED_ARG_V2.format('mistake_score_col_name', 'str')}"
    assert isinstance(rules, LQRules) and rules, f"{REQUIRED_ARG_V2.format('rules', 'str')}"
    return dataset_id

