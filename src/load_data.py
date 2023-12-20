import os
import yaml
import argparse
from get_data import get_data, read_yaml


def load_data(config_path):
    config = read_yaml(config_path)
    df = get_data(config_path)
    new_cols = [col.replace(" ","_") for col in df.columns]
    raw_data_path = config['load_data']['raw_folder_path']
    df.to_csv(raw_data_path, sep = ',', index=False, header=new_cols)
    #df added


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    load_data(config_path = parsed_args.config)