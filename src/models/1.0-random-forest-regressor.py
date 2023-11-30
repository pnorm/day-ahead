from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
# from sklearn.preprocessing import MinMaxScaler, StandardScaler, QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger


df = pd.read_csv("../../data/processed/electricity.csv", index_col='date')

df_filtered = df[df.index <= '2023-11-28'].copy()

# Preparing the data for feature importance analysis
X = df_filtered.drop('OT', axis=1)
y = df_filtered['OT']

# Selecting a target variable for prediction. Assuming it to be 'BEL' for this example.
target = 'OT'

# Dropping the date column as it is not a feature and separating features and target
X = df_filtered.drop('OT', axis=1)
y = df_filtered['OT']

# Splitting the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a pipeline with feature selection and a RandomForestRegressor
pipeline = Pipeline([
    ('feature_selection', SelectKBest(score_func=f_regression, k=10)),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Fitting the pipeline to the training data
pipeline.fit(X_train, y_train)

# Predicting on the test data
y_pred = pipeline.predict(X_test)

# Calculating metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

logger.debug(mse, r2)

