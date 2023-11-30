import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import Pipeline

from data_preparation import split_data


# Load and scale load iris data
X_train, X_test, y_train, y_test = split_data()


def create_model():
    # Creating a pipeline with feature selection and a RandomForestRegressor
    X_train, X_test, y_train, y_test = split_data()
    
    pipeline = Pipeline([
        ('feature_selection', SelectKBest(score_func=f_regression, k=10)),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Fitting the pipeline to the training data
    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, "model_random_forest_regressor.joblib")