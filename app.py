from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

EMAIL_PENGIRIM = "forfunbrother48@gmail.com"
APP_PASSWORD = "iulr teja jhnr eqwe"  # APP PASSWORD, BUKAN PASSWORD AKUN

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        subject = request.form.get("subject")
        body = request.form.get("body")
        emails_raw = request.form.get("emails")

        email_list = [e.strip() for e in emails_raw.splitlines() if e.strip()]

        if len(email_list) > 300:
            message = "❌ Maksimal 300 email"
        else:
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
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
                message = f"✅ Berhasil mengirim ke {len(email_list)} email"

            except Exception as e:
                message = f"❌ Error: {e}"

    return render_template("index.html", message=message)

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)
