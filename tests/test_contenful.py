from datetime import datetime
from constants import TIME_FORMAT
from contentful_utils import environment, archive_messages
from actions import build_and_publish_post


def test_new_message_creation():
    entry = {
        "content_type_id": "whatsAppMessage",
        "fields": {
            "body": {"en-US": "hey there this is looking fly"},
            "received": {"en-US": datetime.now().strftime(TIME_FORMAT)},
        },
    }

    environment.entries().create("new_message2", entry)


def test_new_post_creation():
    included_messages = build_and_publish_post()
    archive_messages(included_messages)