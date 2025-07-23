
from sendgrid import SendGridAPIClient, Mail
from sendgrid.helpers.mail import Mail
from dash import state

config = state.config()
client = SendGridAPIClient(config.SENDGRID_API_KEY)

def send(subject: str, message: str, email: str):
    message = Mail(
        from_email=config.FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=message.replace('\n', '<br>')
    )

    response = client.send(message)

    if response.status_code > 300:
        raise Exception(f'{response.body} ({response.status_code})')

    return response
