import smtplib
from email.mime.text import MIMEText
from .config import Config

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = Config.SMTP_USER
    msg['To'] = Config.SMTP_USER
    
    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(msg)
