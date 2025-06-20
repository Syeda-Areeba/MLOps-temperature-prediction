import mlflow
from mlflow.models import infer_signature
import pandas as pd
import math
# from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the Iris dataset
processed_df = pd.read_csv('../data/processed_weather_data.csv')

# Split the data into training and test sets
X = processed_df.drop(columns=['Temperature (°C)'])
y = processed_df['Temperature (°C)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model hyperparameters
# params = {
#         "solver": "lbfgs",
#         "max_iter": 1000,
#         "multi_class": "auto",
#         "random_state": 8888,
#     }

# Train the model
# lr = LinearRegression(**params)
lr = LinearRegression()
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Set our tracking server uri for logging
mlflow.set_tracking_uri(uri="http://127.0.0.1:9000")

# Create a new MLflow Experiment
mlflow.set_experiment("Weather Prediction")

# Start an MLflow run
with mlflow.start_run():
    # Log the hyperparameters
    # mlflow.log_params(params)

    # Log the loss metric
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    # Set a tag that we can use to remind ourselves what this run was for
    mlflow.set_tag("Training Info", "Basic LR model for live weather data")

    # Infer the model signature
    signature = infer_signature(X_train, lr.predict(X_train))

    # Log the model
    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        artifact_path="weather_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="tracking-weather-prediciton-model",
    )


# Load the model back for predictions as a generic Python Function model
loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)

predictions = loaded_model.predict(X_test)

result = pd.DataFrame(X_test)
result["actual_class"] = y_test
result["predicted_class"] = predictions

result[:4]
