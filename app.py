from flask import Flask, render_template, request
import joblib
from utils.extract_features import extract_features

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    features_df = extract_features(url)
    prediction = model.predict(features_df)[0]
    result = "Legitimate Website ✅" if prediction == 0 else "Phishing Website 🚨"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)