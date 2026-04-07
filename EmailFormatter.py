from email.message import EmailMessage
import base64
def create_message(sender ,to , subject, message_text):
    message = EmailMessage()
    message.set_content(message_text)

    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject

    # The API requires the message to be base64url encoded
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': encoded_message}