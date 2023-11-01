from pathlib import Path
import os
import base64
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email.mime.text import MIMEText

from .util import get_secret, load_secrets


#PATH
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIAL_FILEPATH = os.path.join(BASE_DIR, ".secrets", "googleService.json")
SECRETS_FILEPATH = os.path.join(BASE_DIR, ".secrets", ".mail.json")


# Gmail API
secrets = load_secrets(SECRETS_FILEPATH)

SCOPES = [get_secret("SCOPES", secrets)]
print(SCOPES)
FROM_EMAIL = get_secret("FROM_EMAIL", secrets)


def send_code_mail_signup(email, code):
    subject = "[Cooluid] 이메일을 인증해 주세요."
    message = f"회원가입을 원하신다면 아래 링크로 이동해주세요~!.\n http://localhost:3000/register?code={code}"

    send_email_via_gmail(to=email, subject=subject, message_text=message)


def send_code_mail_signin(email, code):
    subject = "[Cooluid] 이메일을 인증해 주세요."
    message = f"로그인을 원하신다면 아래 링크로 이동해주세요~!.\n http://localhost:3000/email_signin?code={code}"

    send_email_via_gmail(to=email, subject=subject, message_text=message)


def send_email_via_gmail(to, subject, message_text):
    service = get_gmail_service()
    message = create_message(to, subject, message_text)

    try:
        message = (service.users().messages().send(userId='me', body=message).execute())
        print(f"Message Id: {message['id']}")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_gmail_service(user_id = FROM_EMAIL):
    credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_FILEPATH, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(user_id)

    return build('gmail', 'v1', credentials=delegated_credentials)


def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    email_message = {'raw': raw_message}

    return email_message


