import os

import resend
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()  # reads .env in local dev; in production, set real env vars instead

app = Flask(__name__)

SECTIONS = ["about", "projects", "skills", "resume", "contact"]

# --- Mail config (Resend — works over HTTPS, so it isn't blocked by
# Render's free-tier outbound SMTP restriction) ---
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
MAIL_FROM = os.environ.get("MAIL_FROM", "onboarding@resend.dev")
MAIL_TO = os.environ.get("MAIL_TO")

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


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

    if not RESEND_API_KEY or not MAIL_TO:
        app.logger.error("Contact form submitted but RESEND_API_KEY/MAIL_TO are not set.")
        return render_template(
            "partials/contact_error.html",
            error="Message could not be sent — mail isn't configured yet.",
        ), 500

    safe_message = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    try:
        resend.Emails.send({
            "from": MAIL_FROM,
            "to": MAIL_TO,
            "reply_to": email,
            "subject": f"Portfolio contact form — {name}",
            "html": f"<p><strong>From:</strong> {name} &lt;{email}&gt;</p><p>{safe_message}</p>",
        })
    except Exception as exc:
        app.logger.error(f"Failed to send contact form email: {exc}")
        return render_template(
            "partials/contact_error.html",
            error="Something went wrong sending your message — please try again.",
        ), 500

    return render_template("partials/contact_success.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)