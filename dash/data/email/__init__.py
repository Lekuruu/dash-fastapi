
from asyncio import get_running_loop
from importlib import import_module
from dash import state, logger
from types import ModuleType

VALID_PROVIDERS = (
    'smtp',
    'sendgrid',
    'mailgun'
)

def send(
    subject: str,
    message: str,
    email: str,
    retries: int = 0
) -> None:
    """Send an email to the specified address."""
    logger.debug(f'Trying to send email to {email} with subject "{subject}"...')
    config = state.config()

    if config.EMAIL_PROVIDER not in VALID_PROVIDERS:
        logger.warning('Emails are not available. Skipping...')
        return

    if not (provider := resolve_email_provider()):
        logger.error('Email provider not found.')
        return

    try:
        provider.send(subject, message, email)
    except Exception as e:
        if retries > 2:
            logger.error(f'Failed to send email to {email} with subject "{subject}".')
            return

        logger.warning(f'Failed to send email: "{e}" Retrying...')
        return send(subject, message, email, retries + 1)

async def send_async(
    subject: str,
    message: str,
    email: str
) -> None:
    """Send an email to the specified address, asynchronously."""
    await get_running_loop().run_in_executor(
        None, send,
        subject, message, email
    )

def resolve_email_provider() -> ModuleType | None:
    """Resolve the email provider module based on the app configuration."""
    try:
        config = state.config()
        module = import_module(f'dash.data.email.{config.EMAIL_PROVIDER}')

        if not hasattr(module, 'send'):
            logger.error(f'Provider {config.EMAIL_PROVIDER} does not have a send method.')
            return

        return module
    except ImportError:
        logger.error(
            f"Failed to import provider '{config.EMAIL_PROVIDER}'. "
            f"Ensure that you used a valid provider name."
        )
