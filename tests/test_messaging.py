import twilio_utils, messages
from models import ContentfulUser

test_user = ContentfulUser(number="whatsapp:+15149969478")


def test_send_name_message():
    twilio_utils.send_message(messages.Onboarding.need_name, user=test_user)


def test_send_location_message():
    twilio_utils.send_message(messages.Onboarding.need_location, user=test_user)


def test_send_complete_message():
    [twilio_utils.send_message(m, user=test_user) for m in messages.Onboarding.onboarding_complete]
