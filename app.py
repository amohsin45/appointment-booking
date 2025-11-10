from flask import Flask, render_template, request
from flask_mail import Mail, Message
from threading import Thread
import traceback
import os
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_TIMEOUT'] = 10  # Prevent hanging (10 seconds)

mail = Mail(app)

# Async email sending
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("✅ Email sent successfully!")
        except Exception as e:
            print("❌ Email sending failed:")
            traceback.print_exc()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    name = email = message = None
    if request.method == 'POST':
        print("Contact form submitted!")  # Debug
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Contact data: {name}, {email}")  # Debug

        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=['Hasan.mohsin4477@gmail.com'],
            reply_to=email
        )
        msg.body = f"Name: {name}\nClient Email: {email}\nMessage:\n{message}"

        print("Sending contact email...")
        Thread(target=send_async_email, args=(app, msg)).start()

        return render_template('thank_you.html', name=name)
    return render_template('contact.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        print("Appointment form submitted!")  # Debug
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')
        service = request.form.get('service')
        print(f"Appointment data: {name}, {email}, {date}, {time}, {service}")  # Debug

        msg = Message(
            subject=f"New Appointment Booking from {name}",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=['Hasan.mohsin4477@gmail.com'],
            reply_to=email
        )
        msg.body = f"""
A new appointment has been booked.

Name: {name}
Client Email: {email}
Service: {service}
Date: {date}
Time: {time}
"""

        print("Sending appointment email...")
        Thread(target=send_async_email, args=(app, msg)).start()

        return render_template('appointment_confirm.html', name=name, date=date, time=time, service=service)

    return render_template('appointment.html')

@app.route('/test-email')
def test_email():
    msg = Message(
        subject="Test Email from HM Financial Group",
        recipients=['Hasan.mohsin4477@gmail.com'],
        body="This is a test email sent using Gmail SMTP and Flask."
    )
    try:
        mail.send(msg)
        return "✅ Test email sent successfully!"
    except Exception as e:
        traceback.print_exc()
        return f"❌ Failed to send test email: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5001)