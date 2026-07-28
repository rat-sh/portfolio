import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()  # reads .env in local dev; in production, set real env vars instead

app = Flask(__name__)

SECTIONS = ["about", "projects", "skills", "resume", "contact"]

# --- Mail config (all from environment variables — see .env.example) ---
MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")   # the account that SENDS the email
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")   # app password, not your real password
MAIL_TO = os.environ.get("MAIL_TO", MAIL_USERNAME)  # where contact-form messages land


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/partial/<section>")
def partial(section):
    if section not in SECTIONS:
        return "Not found", 404
    return render_template(f"partials/{section}.html")


@app.route("/contact/submit", methods=["POST"])
def contact_submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return render_template(
            "partials/contact_error.html",
            error="Please fill in every field.",
        ), 400

    if not MAIL_USERNAME or not MAIL_PASSWORD:
        # Mail isn't configured yet — fail loudly in dev instead of
        # silently pretending the message was sent.
        app.logger.error("Contact form submitted but MAIL_USERNAME/MAIL_PASSWORD are not set.")
        return render_template(
            "partials/contact_error.html",
            error="Message could not be sent — mail isn't configured yet.",
        ), 500

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio contact form — {name}"
    msg["From"] = MAIL_USERNAME
    msg["To"] = MAIL_TO
    msg["Reply-To"] = email  # so hitting "reply" in your inbox goes to them, not you
    msg.set_content(f"From: {name} <{email}>\n\n{message}")

    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
    except Exception as exc:
        app.logger.error(f"Failed to send contact form email: {exc}")
        return render_template(
            "partials/contact_error.html",
            error="Something went wrong sending your message — please try again.",
        ), 500

    return render_template("partials/contact_success.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
