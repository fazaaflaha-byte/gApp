from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

EMAIL_PENGIRIM = os.environ.get("EMAIL_PENGIRIM")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if request.method == "POST":
        subject = request.form.get("subject")
        body = request.form.get("body")
        emails_raw = request.form.get("emails")

        email_list = [e.strip() for e in emails_raw.splitlines() if e.strip()]

        if len(email_list) > 300:
            message = "❌ Maksimal 300 email"
        else:
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(EMAIL_PENGIRIM, APP_PASSWORD)

                for email in email_list:
                    msg = MIMEMultipart()
                    msg["From"] = EMAIL_PENGIRIM
                    msg["To"] = email
                    msg["Subject"] = subject
                    msg.attach(MIMEText(body, "plain"))
                    server.send_message(msg)

                server.quit()
                message = f"✅ Berhasil kirim ke {len(email_list)} email"

            except Exception as e:
                message = f"❌ Error: {e}"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run()
