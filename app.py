from flask import Flask, render_template, request
import os, joblib
from utils import extract_features  # make sure you have this file

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
    prediction = model.predict(features)[0]

    result = "Unsafe / Fake Website ⚠️" if prediction == 1 else "Safe Website ✅"
    return render_template('index.html', url=url, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
