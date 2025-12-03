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
    print("📧 EMAIL FUNCTION CALLED")

    sender_email = "moulyakrm@gmail.com"
    receiver_email = "moulyakrm@gmail.com"
    password = "jdawfvlcjihwwnnd"

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
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
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


@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']
    print("✅ URL received:", url)

    # 1. Model Prediction
    features = extract_features(url)
    model_result = model.predict(features)[0]   # 0 = phishing, 1 = safe

    # 2. Google Safe Browsing
    google_result = check_with_google_safe_browsing(url)

    # 3. Final decision
    if model_result == 0 or google_result == True:
        final_label = "⚠️ PHISHING WEBSITE DETECTED"
        alert_type = "danger"

        # Send email
        send_alert_email(url)

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
    app.run(host="0.0.0.0", port=10000)
