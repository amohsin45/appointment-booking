from flask import Flask, render_template, request, flash
from threading import Thread
import traceback
import os
from dotenv import load_dotenv
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # ✅ Added for migrations

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

# PostgreSQL Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Render provides this
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ Initialize Flask-Migrate
migrate = Migrate(app, db)

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(50), nullable=False)

# Function to send email using SendGrid API
def send_email(subject, body):
    try:
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {os.environ.get('SENDGRID_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "personalizations": [{
                "to": [{"email": "hasan.mohsin4477@gmail.com"}]  # Admin email
            }],
            "from": {"email": os.environ.get('SENDGRID_SENDER')},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}]
        }
        response = requests.post(url, headers=headers, json=data)
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

        # ✅ Check if slot is already booked
        existing = Appointment.query.filter_by(date=date, time=time).first()
        if existing:
            flash("❌ This time slot is already booked. Please choose another.")
            return render_template('appointment.html')

        # ✅ Save appointment
        new_appointment = Appointment(name=name, email=email, date=date, time=time, service=service)
        db.session.add(new_appointment)
        db.session.commit()

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