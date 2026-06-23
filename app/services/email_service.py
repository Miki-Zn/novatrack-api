from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_welcome_email(email_to: EmailStr, name: str):
    html_content = f"""
    <html>
        <body>
            <h2>Welcome to NovaTrack, {name}!</h2>
            <p>We are excited to have you on board. You can now create projects and manage your tasks efficiently.</p>
            <p>Best regards,<br>The NovaTrack Team</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to NovaTrack!",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)