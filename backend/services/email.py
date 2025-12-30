import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "hello@handled.ai")


def send_magic_link(email: str, link: str) -> None:
    if not SENDGRID_API_KEY:
        raise RuntimeError("SENDGRID_API_KEY is not configured")

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject="Your Handled magic link",
        html_content=f"<p>Click to sign in: <a href=\"{link}\">{link}</a></p>"
    )

    SendGridAPIClient(SENDGRID_API_KEY).send(message)
