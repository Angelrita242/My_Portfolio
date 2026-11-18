import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "change-this-for-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{INSTANCE_DIR / 'messages.db'}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please complete all fields before sending your message.", "error")
        return redirect(url_for("index") + "#contact")

    if len(name) > 200 or len(email) > 200 or len(message) > 5000:
        flash("One or more fields are too long. Please shorten your message.", "error")
        return redirect(url_for("index") + "#contact")

    db.session.add(Message(name=name, email=email, message=message))
    db.session.commit()

    send_email(name, email, message)
    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


def send_email(name, sender_email, message_text):
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_APP_PASSWORD")
    receiver = os.environ.get("MAIL_RECEIVER", username)

    # The contact message is still saved in the database if email is not configured.
    if not username or not password or not receiver:
        app.logger.warning("Email notification is not configured; message saved to database.")
        return

    email_message = EmailMessage()
    email_message["Subject"] = f"New portfolio message from {name}"
    email_message["From"] = username
    email_message["To"] = receiver
    email_message["Reply-To"] = sender_email
    email_message.set_content(
        f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message_text}"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(email_message)
    except (OSError, smtplib.SMTPException):
        app.logger.exception("Unable to send portfolio email notification.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")