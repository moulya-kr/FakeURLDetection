from flask import Flask, render_template, request
import pickle
import numpy as np
from utils.extract_features import extract_features  # make sure utils folder and file exist

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        url = request.form['url']

        # Extract numeric features only (no column names)
        features = extract_features(url)

        # Convert features to numpy array for sklearn
        features_array = np.array(features).reshape(1, -1)

        # Predict using the model
        prediction = model.predict(features_array)[0]

        # Interpret result
        if prediction == 1:
            result = "⚠️ Fake / Phishing Website Detected!"
        else:
            result = "✅ Legitimate (Safe) Website"

        return render_template('index.html', url=url, result=result)


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render assigns the PORT automatically
    app.run(host='0.0.0.0', port=port, debug=False)
