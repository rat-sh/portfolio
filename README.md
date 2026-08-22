# Portfolio

My personal portfolio site — built with Flask on the backend and HTMX on the frontend, so the whole thing runs as a server-rendered app with dynamic section-swapping and no separate JS framework or build step.

## Features

- **HTMX-driven navigation** — About, Projects, Skills, Resume, and Contact sections load dynamically into the page via `hx-get`/`hx-target` without a full page reload
- **Contact form** — sends messages via [Resend](https://resend.com) (HTTPS-based email API, chosen specifically because it isn't blocked by Render's free-tier outbound SMTP restrictions)
- **Resume section** — serves a downloadable resume PDF directly from the site
- **Server-rendered partials** — each section (`about`, `projects`, `skills`, `resume`, `contact`) is its own Jinja2 partial template, fetched on demand

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTMX, vanilla CSS/JS (no frontend build step)
- **Email:** Resend API (with `python-dotenv` for local env config)
- **Server:** Gunicorn (production WSGI server)

## Project Structure

```
portfolio/
├── app.py                          # Flask app + routes
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── resume/rathi-ghosh-resume.pdf
└── templates/
    ├── index.html                  # base page + nav
    └── partials/
        ├── about.html
        ├── projects.html
        ├── skills.html
        ├── resume.html
        ├── contact.html
        ├── contact_success.html
        └── contact_error.html
```

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Renders the base page |
| `/partial/<section>` | GET | Returns the HTML partial for `about`, `projects`, `skills`, `resume`, or `contact` (used by HTMX) |
| `/contact/submit` | POST | Handles contact form submission and sends an email via Resend |

## Getting Started

### Prerequisites
- Python 3
- A [Resend](https://resend.com) API key (for the contact form to actually send mail)

### Installation

```bash
git clone https://github.com/rat-sh/portfolio.git
cd portfolio
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
RESEND_API_KEY=your_resend_api_key
MAIL_FROM=onboarding@resend.dev
MAIL_TO=your_email@example.com
```

- `RESEND_API_KEY` — your Resend API key
- `MAIL_FROM` — sender address Resend sends from (defaults to `onboarding@resend.dev` if unset)
- `MAIL_TO` — the inbox that receives contact form submissions

### Running locally

```bash
python app.py
```

The app runs at `http://localhost:5000` in debug mode.

### Production

The app is configured to run behind Gunicorn:

```bash
gunicorn app:app
```

## License

No license specified yet.
