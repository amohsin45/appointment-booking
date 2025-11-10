from flask import Flask, render_template, request
from threading import Thread
import traceback
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Send email using SendGrid API (SSL verify disabled for local testing)
def send_email(subject, body):
    try:
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {os.environ.get('SENDGRID_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "personalizations": [{"to": [{"email": "hasan.mohsin4477@gmail.com"}]}],
            "from": {"email": os.environ.get('SENDGRID_SENDER')},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}]
        }
        response = requests.post(url, headers=headers, json=data, verify=False)  # Disable SSL check
        print(f"✅ Email sent! Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print("❌ Email sending failed:")
        traceback.print_exc()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        subject = f"New Contact Form Submission from {name}"
        body = f"Name: {name}\nClient Email: {email}\nMessage:\n{message}"

        Thread(target=send_email, args=(subject, body)).start()
        return render_template('thank_you.html', name=name)
    return render_template('contact.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')
        service = request.form.get('service')

        subject = f"New Appointment Booking from {name}"
        body = f"""
A new appointment has been booked.

Name: {name}
Client Email: {email}
Service: {service}
Date: {date}
Time: {time}
"""

        Thread(target=send_email, args=(subject, body)).start()
        return render_template('appointment_confirm.html', name=name, date=date, time=time, service=service)
    return render_template('appointment.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)