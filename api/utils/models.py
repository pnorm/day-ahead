import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import Pipeline

from data_preparation import split_data, load_data


def create_model():
    df = load_data(filtered=True, path="../../data/processed/electricity.csv")
    X_train, X_test, y_train, y_test = split_data(df)
    
    pipeline = Pipeline([
        ('feature_selection', SelectKBest(score_func=f_regression, k=10)),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Fitting the pipeline to the training data
    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, "model_random_forest_regressor.joblib")


if __name__ == "__main__":
    create_model()