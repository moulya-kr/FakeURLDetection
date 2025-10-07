from flask import Flask, render_template, request
import os, joblib
from utils.extract_features import extract_features  # make sure you have this file

app = Flask(__name__)

# Load trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    features = extract_features(url)

    # Convert to 2D array for model input
    import numpy as np
    features = np.array(features).reshape(1, -1)

    prediction = model.predict(features)[0]

    if prediction == 1:
        result = "Fake / Unsafe Website"
    else:
        result = "Safe Website"

    return render_template('index.html', prediction_text=f"Result: {result}")
