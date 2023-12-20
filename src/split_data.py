import os
import yaml
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_yaml

def split_data(config_path):
    config = read_yaml(config_path)
    data_path = config['load_data']['raw_folder_path']
    train_path = config['split_data']['train_path']
    test_path = config['split_data']['test_path']
    split_ratio = config['split_data']['test_size']
    random_state = config['base']['random_state']

    df = pd.read_csv(data_path, sep=',')
    df_train, df_test = train_test_split(
        df,
        test_size= split_ratio, 
        random_state=random_state)
    df_train.to_csv(train_path, sep=',', index=False, encoding='utf-8')
    df_test.to_csv(test_path, sep=',', index=False, encoding='utf-8')

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    split_data(config_path = parsed_args.config)