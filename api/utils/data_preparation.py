from datetime import date, timedelta
import numpy as np
import pandas as pd

from loguru import logger
from sklearn.model_selection import train_test_split


OFFSET_DATE = (date.today() - timedelta(days=3)).isoformat()


def load_data(filtered=True, path="../data/processed/electricity.csv"):
    df = pd.read_csv(path, index_col='date', parse_dates=True)
    if filtered:
        df_filtered = df[df.index < OFFSET_DATE].copy()
        return df_filtered
    return df

def load_features(df, target="OT"):
    return df.drop(target, axis=1)

def load_target(df, target="OT"):
    return df[target]

def split_data(df):
    X = load_features(df)
    y = load_target(df)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def load_data_for_prediction():
    df = load_data(filtered=False)
    df_f = load_features(df)
    today_features = df_f[df_f.index.date == pd.to_datetime(OFFSET_DATE).date()]
    return today_features
