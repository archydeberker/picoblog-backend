from twilio.rest import Client
from constants import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_message(message, user):
    sender = "whatsapp:+14155238886"
    print(user.number)
    message = client.messages.create(
        body=message,
        from_=sender,
        to=user.number,
    )