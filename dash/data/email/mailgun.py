
from requests import Session, Response
from dash import state
from os import environ

config = state.config()
requests = Session()
requests.headers.update({
    'User-Agent': 'solero/dash'
})

EMAIL_DOMAIN = config.FROM_EMAIL.split('@')[-1]
MAILGUN_URL = environ.get('MAILGUN_URL', 'api.eu.mailgun.net')

def mailgun(subject: str, message: str, email: str) -> Response:
    response = requests.post(
        f'https://{MAILGUN_URL}/v3/{config.EMAIL_DOMAIN}/messages',
        auth=('api', config.MAILGUN_API_KEY),
        data={
            'from': f'{config.SITE_NAME} <{config.FROM_EMAIL}>',
            'to': [email],
            'subject': subject,
            'html': message.replace('\n', '<br>')
        }
    )
    response.raise_for_status()
    return response
