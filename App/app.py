from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import os
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# MongoDB setup
# client = MongoClient('mongodb://localhost:27017/')
# client = MongoClient('mongodb://database:27017/')

# db = client['weather_app']
# users_collection = db['users']

# Configure MongoDB URI from environment or fallback to Kubernetes service name
# app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://mongo.default.svc.cluster.local:27017/weather_app')

ENV = os.getenv("FLASK_ENV")  # Default to "production" if FLASK_ENV is not set

# Configure MongoDB URI ased on the environment
if ENV == "production":
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://mongo.default.svc.cluster.local:27017/weather_app')
else:
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/weather_app')

# Initialize MongoDB client
client = MongoClient(app.config['MONGO_URI'])

# Connect to the database
db = client['weather_app']
users_collection = db['users']

print('Environment:', os.getenv('FLASK_ENV'))

with open("./App/models/linear_reg_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("./App/processors/label_encoder.pkl", "rb") as le_file:
    le = pickle.load(le_file)

with open("./App/processors/scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# with open("./models/linear_reg_model.pkl", "rb") as model_file:
#     model = pickle.load(model_file)

# with open("./processors/label_encoder.pkl", "rb") as le_file:
#     le = pickle.load(le_file)

# with open("./processors/scaler.pkl", "rb") as scaler_file:
#     scaler = pickle.load(scaler_file)

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("predict"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username})

        if user and user["password"] == password:
            session["user_id"] = str(user["_id"])
            return redirect(url_for("predict"))
        return "Invalid credentials. Try again."
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users_collection.find_one({"username": username}):
            return "Username already exists. Please choose another."

        users_collection.insert_one({"username": username, "password": password})
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Gather input features from the form
        humidity = float(request.form["humidity"])
        wind_speed = float(request.form["wind_speed"])
        weather_condition = int(request.form["weather_condition"])
        hour = int(request.form["hour"])
        day = int(request.form["day"])
        month = int(request.form["month"])
        day_of_year = int(request.form["day_of_year"])

        # Check if the weather condition exists in the encoder
        if weather_condition not in le.classes_:
            # Add the new label to the LabelEncoder
            le.classes_ = np.append(le.classes_, weather_condition)
            
            # Save the updated LabelEncoder
            with open("./App/processors/updated_label_encoder.pkl", "wb") as le_file:
                pickle.dump(le, le_file)

        # Label encode the weather condition
        weather_condition_encoded = le.transform([weather_condition])[0]

        # Preprocess the input data
        input_data = {
            "Humidity": humidity,
            "Wind Speed": wind_speed,
            "Weather Condition": weather_condition_encoded,
            "Hour": hour,
            "Day": day,
            "Month": month,
            "Day_of_year": day_of_year
        }

        # Standardize the input data
        input_features = np.array([[
            input_data["Humidity"],
            input_data["Wind Speed"],
            input_data["Weather Condition"],
            input_data["Hour"],
            input_data["Day"],
            input_data["Month"],
            input_data["Day_of_year"]
        ]])

        # Scale the input features using the same scaler used during training
        input_scaled = scaler.transform(input_features)

        # Make the prediction
        prediction = model.predict(input_scaled)

        return render_template("prediction.html", prediction=round(prediction[0], 2))

    return render_template("weather_form.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
