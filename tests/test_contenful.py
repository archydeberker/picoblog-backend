from datetime import datetime
from constants import TIME_FORMAT
from contentful_utils import environment, archive_messages, upload_assets_to_contentful
from actions import build_and_publish_post
from models import Media


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


def test_media_creation():
    new_media = Media(url='https://api.twilio.com/2010-04-01/Accounts/AC4fe532def6dbef2698bdf45bda6118fe/Messages/MM1a174bfeb039067dadfc3e6dce72131c/Media/ME3f776cb7a25808dc38c5b6b12235009b',
                      content_type='image/jpeg',
                      title='test_upload2',
                      owner='archy'
                      )

    upload_assets_to_contentful(new_media)