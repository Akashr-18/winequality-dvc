import os
import yaml
import argparse
from get_data import read_yaml
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import json
import joblib

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2= r2_score(actual, pred)
    return rmse, mae, r2

def train_and_evaluate(config_path):
    config = read_yaml(config_path)
    train_data_path = config['split_data']['train_path']
    test_data_path = config['split_data']['test_path']
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    alpha = config['estimators']['ElasticNet']['params']['alpha']
    l1_ratio = config['estimators']['ElasticNet']['params']['l1_ratio']

    target = [config['base']['target_column']]

    df_train = pd.read_csv(train_data_path, sep=',')
    df_test = pd.read_csv(test_data_path, sep=',')

    y_train = df_train[target]
    y_test = df_test[target]

    x_train = df_train.drop(target, axis=1)
    x_test = df_test.drop(target, axis=1)

    lr = ElasticNet(
        alpha=alpha, 
        l1_ratio=l1_ratio,
        random_state=random_state
    )
    lr.fit(x_train, y_train)

    y_pred = lr.predict(x_test)
    (rmse, mae, r2_score) = eval_metrics(y_test, y_pred)

    print("ElasticNet model: (alpha=%f, l1_ratio=%f)" %(alpha, l1_ratio))
    print("RMSE: ", rmse)
    print("MAE: ", mae)
    print("R2 Score: ", r2_score)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir,'model.joblib')

    joblib.dump(lr, model_path)

    scores_file = config['report']['scores']
    variables_file = config['report']['variables']

    sc_dir, sc_file = os.path.split(scores_file)
    var_dir, var_file = os.path.split(variables_file)

    os.makedirs(sc_dir, exist_ok=True)
    os.makedirs(var_dir, exist_ok=True)

    with open(scores_file, 'w') as f:
        pass
    with open(variables_file, 'w') as f:
        pass

    with open(scores_file, 'w') as f:
        scores = {
            'rmse': rmse,
            'mae': mae,
            'r2_score': r2_score
        }
        json.dump(scores, f, indent=4)

    with open(variables_file, 'w') as f:
        variables = {
            'alpha': alpha,
            'l1_ratio': l1_ratio
        }
        json.dump(variables, f, indent=4)

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)