import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import os
import pickle

def preprocess_and_save():
    file_path = os.path.join('/opt/airflow/DVC/data', 'raw_weather_data.csv')
    df = pd.read_csv(file_path)

    df.drop(columns=['Date'], inplace=True)

    df['Time'] = pd.to_datetime(df['Time'])

    df['Hour'] = df['Time'].dt.hour
    df['Day'] = df['Time'].dt.dayofweek
    df['Month'] = df['Time'].dt.month
    df['Day_of_year'] = df['Time'].dt.dayofyear

    df.drop(columns=['Time'], inplace=True)

    le = LabelEncoder()
    df['Weather Condition'] = le.fit_transform(df['Weather Condition'])

    X = df.drop(columns=['Temperature (°C)'])
    y = df['Temperature (°C)']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    processed_df = pd.DataFrame(X_scaled, columns=X.columns)
    processed_df['Temperature (°C)'] = y.reset_index(drop=True)

    processed_file_path = os.path.join('/opt/airflow/DVC/data', 'processed_weather_data.csv')
    processed_df.to_csv(processed_file_path, index=False)
    print("Processed data saved to 'data/processed_weather_data.csv'!")

    with open("/opt/airflow/DVC/processors/scaler.pkl", "wb") as scaler_file:
        pickle.dump(scaler, scaler_file)

    with open("/opt/airflow/DVC/processors/label_encoder.pkl", "wb") as le_file:
        pickle.dump(le, le_file)

preprocess_and_save()