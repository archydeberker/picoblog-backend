from datetime import datetime
from constants import TIME_FORMAT
from contentful_utils import environment, archive_messages, upload_assets_to_contentful, upload_message_to_contentful, \
    find_user
from actions import build_and_publish_post, handle_new_message
from models import TwilioMedia


def test_new_message_creation():
    entry = {
        "content_type_id": "whatsAppMessage",
        "fields": {
            "body": {"en-US": "hey there this is looking fly"},
            "received": {"en-US": datetime.now().strftime(TIME_FORMAT)},
        },
    }

    environment.entries().create("new_message2", entry)


def test_creating_new_message_with_existing_media():
    entry = {
        "content_type_id": "whatsAppMessage",
        "fields": {
            "body": {"en-US": "Can we add media programatically again?"},
            "received": {"en-US": datetime.now().strftime(TIME_FORMAT)},
            # Structure from https://www.contentful.com/developers/docs/concepts/links/#modeling-attachments
            "media": {'en-US': [
                {"sys": {
                    "type": "Link",
                    "linkType": "Asset",
                    "id": 'photo-1598787643262-8cb070483597?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1164&q=80'
                }}
            ]}
        },
    }

    environment.entries().create("new_message_with_media2", entry)


def test_creating_new_message_with_new_media():

    raw_msg = {'Body': 'A nice new test message',
               'From': 'A test number',
               'NumMedia': '1',
               'MediaContentType0': 'img/jpeg',
               'MediaUrl0': 'https://source.unsplash.com/random'}

    handle_new_message(raw_msg)


def test_creating_new_message_with_new_user():
    raw_msg = {'Body': 'A nice new test message',
               'From': 'whatsapp:test_try_again',
               'NumMedia': '0'}

    handle_new_message(raw_msg)


def test_new_post_creation():
    included_messages = build_and_publish_post()
    archive_messages(included_messages)


def test_media_creation():
    new_media = TwilioMedia(
        url="https://api.twilio.com/2010-04-01/Accounts/AC4fe532def6dbef2698bdf45bda6118fe/Messages/MM1a174bfeb039067dadfc3e6dce72131c/Media/ME3f776cb7a25808dc38c5b6b12235009b",
        content_type="image/jpeg",
        title="test_upload2",
        owner="archy",
    )

    upload_assets_to_contentful(new_media)


def test_find_user_when_does_not_exist():
    user = find_user('sdsd')
    assert user is None