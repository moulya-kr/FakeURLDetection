import requests
from flask import Flask, render_template, request
import joblib
from utils.extract_features import extract_features

# Replace with your actual API key from Google
API_KEY = "AIzaSyAv6MRzju5zlERYH87wGKbsULXRlDx6Sm8"

def check_with_google_safe_browsing(url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    body = {
        "client": {
            "clientId": "fake-url-detector",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(api_url, json=body)
    result = response.json()
    print("Google API response:",result)

    # If "matches" key exists, Google marked it unsafe
    if "matches" in result:
        return True
    else:
        return False


app = Flask(__name__)
model = joblib.load('model.pkl')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    # Step 1: Extract features and get model prediction
    features_df = extract_features(url)
    model_prediction = model.predict(features_df)[0]  # 1 = Legitimate, 0 = Phishing

    # Step 2: Check with Google Safe Browsing
    google_flag = check_with_google_safe_browsing(url)  # True = unsafe, False = safe

    # Step 3: Combine both predictions smartly
    if google_flag:
        # Google says it's unsafe → we immediately trust Google
        final_label = "⚠️ Unsafe Website (Flagged by Google Safe Browsing)"
        alert_type = "danger"
    else:
        # Google says safe → trust Google
        if model_prediction == 1:
            final_label = "✅ Safe Website (Confirmed by Google)"
        else:
            final_label = "✅ Safe Website (Google Verified — Model uncertain)"
        alert_type = "success"

    # Step 4: Construct message
    message = f"""
    🌐 URL: {url}<br>
    🧠 Model Prediction: {'Phishing' if model_prediction == 0 else 'Legitimate'}<br>
    🔍 Google Safe Browsing: {'Unsafe' if google_flag else 'Safe'}<br>
    🧾 Final Decision: {final_label}
    """

    return render_template('index.html', prediction_text=message, alert_type=alert_type)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)