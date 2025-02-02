import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Correctly fetch environment variables with a default value
GMAIL_SMTP_SERVER = os.getenv("GMAIL_SMTP_SERVER", "smtp.gmail.com")
GMAIL_SMTP_PORT = int(os.getenv("GMAIL_SMTP_PORT", "587"))  # ✅ Fixed error
GMAIL_USERNAME = os.getenv("titumvposting@gmail.com")
GMAIL_PASSWORD = os.getenv("zbbkdssscyjmszfy")
BLOGGER_EMAIL = os.getenv("asatkarsarvesh39.titu@blogger.com")

def send_email(subject, content):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        # Create email
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USERNAME
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'html'))

        # Send email
        server.sendmail(GMAIL_USERNAME, BLOGGER_EMAIL, msg.as_string())
        server.quit()

        return {"status": "success", "message": "Email sent successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/send_data", methods=["POST"])
def send_data():
    data = request.json

    email_content = f"""
    <h1>{data['title']}</h1>
    <img src='{data['poster']}' width='200'><br>
    <p><b>Cast:</b> {data['cast']}</p>
    <p><b>Release Date:</b> {data['release_date']}</p>
    <p><b>Synopsis:</b> {data['synopsis']}</p>
    <h3>Screenshots:</h3>
    {"".join([f"<img src='{img}' width='150'>" for img in data['screenshots']])}
    <h3>Watch Now:</h3>
    {data['embed_frame']}
    """

    response = send_email(data["title"], email_content)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
