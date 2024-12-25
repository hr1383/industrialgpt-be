from app.config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


api_key = settings.SENDGRID_API_KEY
# try:
class EmailService:

   def send_email(self, text):
        message = Mail(
            from_email='aijobsterworks@gmail.com',
            to_emails=['hrsht.rastogi13@gmail.com'],
            subject='Transcription from the AI Assistant',
            plain_text_content=text)
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

# except Exception as e:
#     print(e.message)
