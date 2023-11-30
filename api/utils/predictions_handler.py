from datetime import date
import joblib
import json
from loguru import logger
import pandas as pd

from .data_preparation import split_data, load_data_for_prediction, load_data, load_features, load_target

@logger.catch()
def get_predictions(model_filename):
    # Load saved model
    model = joblib.load(model_filename)
    logger.debug("Model succesfully loaded.")

    X_test = load_data_for_prediction()
    X_test_dates = X_test.index.to_list()
    dates = [date.isoformat() for date in X_test_dates]
    # Predict class
    y_pred = model.predict(X_test.values)

    y_pred = y_pred.tolist()
    # Combine the lists into a list of dictionaries
    combined_data = [{"date": date, "y": y} for date, y in zip(dates, y_pred)]

    return combined_data


def get_backtest_results(from_date: date, to_date: date, model_filename) -> list:
    start_date = from_date.isoformat()
    end_date = to_date.isoformat() 

    df = load_data(filtered=True)

    # Filter the dataset for the specified date range
    df_filtered = df[start_date:end_date]
    test_dates = df_filtered.index.to_list()
    dates = [date.isoformat() for date in test_dates]

    X = load_features(df_filtered)
    y_true = load_target(df_filtered)
    y_true = y_true.tolist()
    # load model
    model = joblib.load(model_filename)

    # Make predictions
    y_pred = model.predict(X)
    y_pred = y_pred.tolist()

    combined_data = [{"date": date, "y": y, "y_pred": p} for date, y, p in zip(dates, y_true, y_pred)]


    return combined_data