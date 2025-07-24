
import logging

logger = logging.getLogger("emails")

def send(subject: str, message: str, email: str) -> None:
    logger.info(
        f"'{subject}' -> {email}\n"
        f"{message}"
    )
