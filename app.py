import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from flask import Flask, render_template, request
import joblib
from utils.extract_features import extract_features

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

GOOGLE_API_KEY = "AIzaSyCTfy8lUSVEhuXlEBRhKN3qPNZGpDIzJYc"
GOOGLE_API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
def send_email_alert(url, result):
    sender_email = "moulyakrm@gmail.com"
    receiver_email = "moulyakrm@gmail.com"
    password = "jdawfvlcjihwwnnd"

    subject = " Alert! Malicious URL Detected"

    message = f"""
    WARNING!

    A suspicious / phishing URL was detected.

    URL: {url}
    Result: {result}

    Please be cautious.
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'plain','utf-8'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email alert sent successfully!")
    except Exception as e:
        print("email failed:",e)

def send_alert_email(url):
    print("📧 EMAIL FUNCTION CALLED")

    sender_email = "moulyakrm@gmail.com"
    receiver_email = "moulyakrm@gmail.com"
    password = "jdawfvlcjihwwnnd"   # 16-char, no spaces

    message = f"""Subject:  Phishing URL Detected

WARNING!

The following dangerous website was detected:

{url}

Avoid opening it.
"""

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()

        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("❌ EMAIL FAILED:", e)

def check_with_google_safe_browsing(url):
    try:
        payload = {
            "client": {
                "clientId": "fake-url-detector",
                "clientVersion": "1.0"
            },
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

        return False  # Safe
    except Exception as e:
        print("Google API Error:", e)
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    # Step 1
    features_df = extract_features(url)
    model_prediction = model.predict(features_df)[0]  # 1 Legit, 0 Phishing

    # Step 2
    google_flag = check_with_google_safe_browsing(url)  # True/False

    # Step 3
    if google_flag:
        final_label = "⚠️ Unsafe Website (Flagged by Google Safe Browsing)"
        alert_type = "danger"

        print("EMAIL FUNCTION CALLED")
        send_email_alert(url, final_label)
    else:
        final_label = "✅ SAFE WEBSITE"
        alert_type = "success"

    return render_template(
        "index.html",
        prediction_text=final_label,
        alert_type=alert_type,
        url=url
    )
if __name__ == "__main__":
    send_alert_email("http://testsafebrowsing.appspot.com/s/malware.html")