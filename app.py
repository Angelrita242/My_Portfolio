from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# DATABASE MODEL
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    message = db.Column(db.Text)

# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")

# FORM SUBMISSION
@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # Save to DB
    msg = Message(name=name, email=email, message=message)
    db.session.add(msg)
    db.session.commit()

    # Send email notification
    send_email(name, email, message)

    return redirect("/success")

# SUCCESS PAGE
@app.route("/success")
def success():
    return render_template("success.html")


# EMAIL SENDER
def send_email(name, email, message):
    sender = "justangelrita@gmail.com"
    password = "likzhxhorzxclyyr"
    receiver = "justangelrita@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = f"New message from {name}"
    msg['From'] = sender
    msg['To'] = receiver
    msg['Reply-To'] = email
    msg.set_content(f"Name: {name}\nEmail: {email}\nMesssage: {message}")



    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email error:", e)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)