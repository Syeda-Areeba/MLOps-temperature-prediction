import json
import csv
import os

def extract_weather_data_to_csv():
    json_file_path = os.path.join('/opt/airflow/DVC/data', 'raw_weather_data.json')
    with open(json_file_path, "r") as json_file:
        weather_data = json.load(json_file)

    extracted_data = []

    if "forecast" in weather_data:
        forecast_days = weather_data["forecast"].get("forecastday", [])

        for day in forecast_days:
            date = day.get("date", "N/A")
            hourly_data = day.get("hour", [])

            for hour in hourly_data:
                time = hour.get("time", "N/A")
                condition = hour.get("condition", {}).get("text", "N/A")
                temperature = hour.get("temp_c", "N/A")
                humidity = hour.get("humidity", "N/A")
                wind_speed = hour.get("wind_kph", "N/A")

                extracted_data.append([date, time, temperature, humidity, wind_speed, condition])
    else:
        print("No 'forecast' field found in the data.")
        return

    csv_file_path = os.path.join('/opt/airflow/DVC/data', 'raw_weather_data.csv')
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Date", "Time", "Temperature (°C)", "Humidity (%)", "Wind Speed (kph)", "Weather Condition"])
        csv_writer.writerows(extracted_data)

    print(f"Weather data has been successfully saved to {csv_file_path}")

extract_weather_data_to_csv()