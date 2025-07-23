
from email.mime.text import MIMEText
from smtplib import SMTP
from dash import state

def send(subject: str, message: str, email: str) -> None:
    config = state.config()

    with SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
        msg = MIMEText(message, 'html')
        msg['Subject'] = subject
        msg['From'] = config.FROM_EMAIL
        msg['To'] = email
        smtp.starttls()
        smtp.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        smtp.sendmail(config.FROM_EMAIL, [email], msg.as_string())
