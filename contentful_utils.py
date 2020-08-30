import random
from datetime import datetime
from typing import List

import contentful_management
from contentful import Entry

from constants import (
    CONTENTFUL_WHATSAPP_TYPE,
    CONTENTFUL_POST_TYPE,
    TIME_FORMAT,
    CONTENTFUL_TOKEN,
    CONTENTFUL_SPACE,
    CONTENTFUL_ENVIRONTMENT_ID,
)
from models import WhatsAppMessage, Post, Media

client = contentful_management.Client(CONTENTFUL_TOKEN)

environment = client.environments(CONTENTFUL_SPACE).find(CONTENTFUL_ENVIRONTMENT_ID)


def generate_new_entry_id():
    return str(random.randint(1, 1000))


def upload_assets_to_contentful(media: Media):
    """
    Before we're able to create a post with attached media objects, we need to upload the asset to Contentful and
    retrieve an asset ID for it. We can then use that ID to attach images to posts.
    :param post:
    :return:
    """
    if media is None:
        return

    file_attributes = {
        "fields": {
            "file": {
                "en-US": {
                    "fileName": media.title,
                    "contentType": media.content_type,
                    "upload": media.url,
                }
            },
            "title": {"en-US": media.title},
            "description": {"en-US": media.owner},
        }
    }

    new_asset = environment.assets().create(media.title, file_attributes)

    new_asset.process()
    new_asset.publish()


def get_all_unpublished_messages():
    messages = environment.entries().all()
    return [
        m
        for m in messages
        if m.content_type.id == CONTENTFUL_WHATSAPP_TYPE and not m.is_archived
    ]


def upload_message_to_contentful(message: WhatsAppMessage):
    new_entry = {
        "content_type_id": CONTENTFUL_WHATSAPP_TYPE,
        "fields": {
            "body": {"en-US": message.body},
            "from": {"en-US": message.sender},
            "received": {"en-US": datetime.now().strftime(TIME_FORMAT)},
        },
    }

    new_entry = environment.entries().create(generate_new_entry_id(), new_entry)

    new_entry.save()


def archive_messages(messages: List[Entry]):
    for entry in messages:
        if entry.is_published:
            entry.unpublish()
        try:
            entry.archive()
        except Exception as e:
            print(e)
            print("Failed to archive")


def upload_post_to_contentful(post: Post):
    new_entry = {
        "content_type_id": CONTENTFUL_POST_TYPE,
        "fields": {
            "body": {"en-US": post.body},
            "title": {"en-US": post.title},
            "slug": {"en-US": post.slug},
            "publishDate": {"en-US": datetime.now().strftime(TIME_FORMAT)},
        },
    }

    new_entry = environment.entries().create(generate_new_entry_id(), new_entry)

    new_entry.save()
    new_entry.publish()


if __name__ == "__main__":
    spaces = client.spaces().all()
    assets = client.assets(CONTENTFUL_SPACE, CONTENTFUL_ENVIRONTMENT_ID).all()
    print(assets)
    entries = client.entries(CONTENTFUL_SPACE, CONTENTFUL_ENVIRONTMENT_ID).all()
    most_recent = entries[0]
    print(most_recent)
