import pandas as pd
import numpy as np
from config import PATH_TO_DATA
import os


def load_prep_data(path: str):
    """
        Takes path to csv file, cleans and returns it back
    """
    data = pd.read_csv(path, sep='|', low_memory=False)
    values = np.where(
        (data['statusCode'] == 200) | (data['statusCode'] == 503) | (data['statusCode'] == 502) |
        (data['statusCode'] == '200') | (data['statusCode'] == '503') | (
                data['statusCode'] == '502'))[0]
    data = data.iloc[values]
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data = data.dropna()
    data['statusCode'] = data['statusCode'].astype('int')
    data = data.sort_values(by='timestamp').reset_index(drop=True)
    assert (data['timestamp'].max() - data['timestamp'].min()).days == 0, 'In the file dates more than 1 day'
    assert data['timestamp'].dtype == 'datetime64[ns]', 'Wrong timestamp type'
    return data


def save_group_by_sec_data(data, save_file_path):
    """
        Gets cleaned data, makes new binary feature 'fault' - 1 for 502 and 503 responses, 0 for 200 response.
        Saves to new csv file.
    """
    def extract_sec_min_hour(x):
        return x.second, x.minute, x.hour

    data['fault'] = np.where((data['statusCode'] == 502) | (data['statusCode'] == 503), 1, 0)
    data['second'], data['minute'], data['hour'] = zip(*data['timestamp'].apply(lambda x: extract_sec_min_hour(x)))
    data.groupby(['hour', 'minute', 'second'])['fault'].agg(['count', 'sum']). \
        reset_index()[['count', 'sum']].to_csv(os.path.join(PATH_TO_DATA, save_file_path), index=False)
