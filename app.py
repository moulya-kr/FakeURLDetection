import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from flask import Flask, render_template, request
import joblib
from utils.extract_features import extract_features

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

GOOGLE_API_KEY = "AIzaSyCTfy8lUSVEhuXlEBRhKN3qPNZGpDIzJYc"
GOOGLE_API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"


# ---------------- EMAIL ALERT ----------------
def send_alert_email(url):
    print("📧 EMAIL FUNCTION CALLED for:", url)

    sender_email = "moulyakrm@gmail.com"
    receiver_email = "moulyakrm@gmail.com"
    password = "YOUR_NEW_APP_PASSWORD"

    subject = "⚠️ PHISHING WEBSITE ALERT"

    body = f"""
WARNING! A dangerous URL was detected.

URL: {url}

Do NOT open this link.
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("🔄 Connecting to Gmail server...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        print("🔐 Logging in...")
        server.login(sender_email, password)
        print("📨 Sending message...")
        server.send_message(msg)
        server.quit()
        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("❌ EMAIL FAILED:", e)


# ------------- GOOGLE SAFE BROWSING ----------------
def check_with_google_safe_browsing(url):
    try:
        payload = {
            "client": {"clientId": "fake-url-detector", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        params = {"key": GOOGLE_API_KEY}
        response = requests.post(GOOGLE_API_URL, params=params, json=payload)
        data = response.json()

        if "matches" in data:
            return True   # Unsafe
        return False

    except Exception as e:
        print("Google API Error:", e)
        return False


# -------------- ROUTES -----------------
@app.route('/')
def home():
    return render_template('index.html')

import pandas as pd
import numpy as np

@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']
    print("\n✅ URL received:", url)

    # Basic check for valid URL
    if not url.startswith("http"):
        return render_template(
            "index.html",
            prediction_text="❌ Invalid URL (must start with http or https)",
            alert_type="danger",
            url=url
        )

    # 1. Extract features
    features = extract_features(url)   # <-- NOW features is defined
    print("📌 Extracted Features:\n", features)

    # 2. Model probability
    prob = model.predict_proba(features)[0][1]   # phishing probability
    prediction = model.predict(features)[0]

    print("🤖 Model Prediction (0=safe, 1=phishing):", prediction)
    print("🔢 Phishing Probability:", prob)

    # 3. Google Safe Browsing check
    unsafe_google = check_with_google_safe_browsing(url)
    print("🌐 Google Unsafe?:", unsafe_google)

    # 4. Final SMART DECISION
    if prob > 0.8:
        result_text = "⚠️ Phishing Website"
        alert_type = "danger"
        send_alert_email(url)

    elif unsafe_google and prob > 0.4:
        result_text = "⚠️ Phishing Website"
        alert_type = "danger"
        send_alert_email(url)

    else:
        result_text = "✅ Legitimate Website"
        alert_type = "success"

    print("✅ Final Result:", result_text)

    return render_template(
        "index.html",
        prediction_text=result_text,
        alert_type=alert_type,
        url=url
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
