import os
import yaml
import argparse
import pandas as pd

def read_yaml(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config

def get_data(config_path):
    config = read_yaml(config_path)
    df_path = config['datasource']['blob_source']
    df = pd.read_csv(df_path, sep=',', encoding='utf8')
    return df

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default="params.yaml")
    parsed_args = args.parse_args()
    data = get_data(config_path = parsed_args.config)