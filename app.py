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
    result = 'Legitimate Website' if prediction == 1 else 'Phishing Website'

    # Pass a flag to the template to trigger alert
    alert_type = 'success' if result == 'Legitimate Website' else 'danger'
    return render_template('index.html', prediction_text=result, alert_type=alert_type, url=url)


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)