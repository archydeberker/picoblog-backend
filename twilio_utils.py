from twilio.rest import Client
from constants import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

sender = "whatsapp:+14155238886"
recipient = "+15149969478"
message = client.messages.create(
    body="Your appointment is coming up on July 21 at 3PM",
    from_=sender,
    to=f"whatsapp:{recipient}",
)
print(message.sid)
