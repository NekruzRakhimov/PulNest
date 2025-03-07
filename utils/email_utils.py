import smtplib
from email.mime.text import MIMEText

from configs.config import settings

def send_email(to_email: str, subject: str, body: str):
    sender_email = settings.email_credentials.email
    sender_password = settings.email_credentials.password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL ('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")




