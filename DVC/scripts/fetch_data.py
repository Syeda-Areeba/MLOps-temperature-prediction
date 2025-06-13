import http.client
import json
from dotenv import load_dotenv
import os

def fetch_weather_data(location="Islamabad", start_date="2024-11-19", end_date="2024-11-26"):
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    load_dotenv()
    api_key = os.getenv("API_KEY")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }

    url = f"/history.json?q={location}&lang=en&dt={start_date}&end_dt={end_date}"

    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()
    
    data_json = json.loads(data.decode("utf-8"))

    output_file = os.path.join('/opt/airflow/DVC/data', 'raw_weather_data.json')
    with open(output_file, "w") as json_file:
        json.dump(data_json, json_file, indent=4)

    print(f"Weather data saved to {output_file}")

fetch_weather_data()