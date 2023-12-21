import os
import yaml
import joblib
import json
import numpy as np

config_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json")

class NotInRange(Exception):
    def __init__(self, message="Values enteres not in range"):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message="Not in cols"):
        self.meassage = message
        super().__init__(self.message)

def read_yaml(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_schema(schema_path = schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def predict(data):
    config = read_yaml(config_path)
    model_dir = config['webapp_model_dir']
    model = joblib.load(model_dir)
    prediction = model.predict(data).tolist()[0]
    try:
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result"

def validate_input(dict_request):
    def validate_cols(col):
        schema = get_schema()
        actual_columns = schema.keys()
        if col not in actual_columns:
            raise NotInCols
        
    def validate_values(col,val):
        schema = get_schema()
        if not (schema[col]['min'] <= float(dict_request[col]) <= schema[col]['max']):
            raise NotInRange

    for col, val in dict_request.items():
        validate_cols(col),
        validate_values(col, val)

    return True

def form_response(dict_request):
    try:
        if validate_input(dict_request):
            data = dict_request.values()
            print("Data1: ", data)   #dict_values(['0', '0'...])
            data = [list(map(float, data))]
            print("Data2: ", data)   #[[0.0,0.0....]]
            response = predict(data)
            return response
        
    except NotInRange as e:
        response = {'expected_range': get_schema(),
                    'response':str(e)}
        return response
    
    except Exception as e:
        response = {'response':str(e)}
        return response

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {'response': response}
            return response
         
    except NotInRange as e:
        response = {'expected_range': get_schema(),
                    'response':str(e)}
        return response
    
    except NotInCols as e:
        response = {'expected_cols':get_schema().keys(),
                    'response':str(e)}
        return response
    
    except Exception as e:
        response = {'response':str(e)}
        return response

