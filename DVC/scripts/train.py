import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import math
import pickle
import json

def train_model():
    processed_df = pd.read_csv('./data/processed_weather_data.csv')

    X = processed_df.drop(columns=['Temperature (°C)'])
    y = processed_df['Temperature (°C)']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = math.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "r_squared": r2,
        "mse": mse,
        "rmse": rmse
    }

    print(f'Mean Squared Error: {mse}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'R-squared: {r2}')
    
    metrics_path = './report/metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    model_path = './models/linear_reg_model.pkl'
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved as {model_path}")

train_model()