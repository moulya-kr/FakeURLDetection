import smtplib

sender_email = "moulyakrm@gmail.com"
password = "jdawfvlcjihwwnnd"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    print("✅ LOGIN SUCCESS")
    server.quit()
except Exception as e:
    print("❌ LOGIN FAILED:", e)
