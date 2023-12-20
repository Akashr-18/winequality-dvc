import os
import yaml
import joblib
import numpy as np

config_path = "params.yaml"

def read_yaml(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_yaml(config_path)
    model_dir = config['webapp_model_dir']
    model = joblib.load(model_dir)
    prediction = model.predict(data).tolist()[0]
    return prediction

def form_response(dict_request):
    data = dict_request.values()
    print("Data1: ", data)
    data = [list(map(float, data))]
    print("Data2: ", data)
    response = predict(data)
    return response

def api_response(dict_request):
    print("Data3: ", dict_request)
    data = np.array([list(dict_request.values())])
    response = predict(data)
    response = {'response': response}
    return response 

