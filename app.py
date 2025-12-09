import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from flask import Flask, render_template, request
import joblib
from utils.extract_features import extract_features
import os

app = Flask(__name__)

model = joblib.load("model.pkl")

GOOGLE_API_KEY = "AIzaSyCTfy8lUSVEhuXlEBRhKN3qPNZGpDIzJYc"
GOOGLE_API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

# EMAIL ALERT
def send_alert_email(url):
    sender = "moulyakrm@gmail.com"
    receiver = "moulyakrm@gmail.com"
    password = "jdawfvlcjihwwnnd"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "⚠️ PHISHING ALERT"
    msg.attach(MIMEText(f"Suspicious URL detected:\n\n{url}", "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("✅ EMAIL SENT")
    except Exception as e:
        print("❌ EMAIL FAILED:", e)


# GOOGLE SAFE BROWSING
def check_with_google_safe_browsing(url):
    payload = {
        "client": {"clientId": "fake-url-detector", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    params = {"key": GOOGLE_API_KEY}
    response = requests.post(GOOGLE_API_URL, params=params, json=payload)

    data = response.json()
    return "matches" in data


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    print("\nURL received:", url)

    if not url.startswith("http"):
        return render_template("index.html",
                               prediction_text="❌ Invalid URL (must start with http OR https)",
                               alert_type="danger",
                               url=url)

    features = extract_features(url)
    model_pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]

    google_flag = check_with_google_safe_browsing(url)

    # FINAL DECISION LOGIC
    if google_flag or prob > 0.80:
        result = "⚠️ Phishing Website"
        alert_type = "danger"
        send_alert_email(url)
    else:
        result = "✅ Legitimate Website"
        alert_type = "success"

    return render_template("index.html",
                           prediction_text=result,
                           alert_type=alert_type,
                           url=url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
