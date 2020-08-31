import random
import time
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
from models import TwilioWhatsAppMessage, ContentfulPost, TwilioMedia

client = contentful_management.Client(CONTENTFUL_TOKEN)

environment = client.environments(CONTENTFUL_SPACE).find(CONTENTFUL_ENVIRONTMENT_ID)


def generate_new_entry_id():
    return str(int(datetime.now().strftime("%Y%m%d%H%M%S")))


def upload_assets_to_contentful(media: TwilioMedia):
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

    # For some reason we have to re-retrieve the asset? Wait 5 seconds to allow it to be uploaded first.
    time.sleep(5)
    asset = environment.assets().find(new_asset.title)
    print(f"Asset to be published is {asset}")
    asset.publish()

    # Wait for publishing to take effect before returning
    time.sleep(5)

    return asset.id


def get_all_unpublished_messages():
    messages = environment.entries().all()
    return [m for m in messages if m.content_type.id == CONTENTFUL_WHATSAPP_TYPE and not m.is_archived]


def upload_message_to_contentful(message: TwilioWhatsAppMessage):
    fields = {
        "body": {"en-US": message.body},
        "from": {"en-US": message.sender},
        "received": {"en-US": datetime.now().strftime(TIME_FORMAT)},
    }

    if message.media:
        fields.update({"media": {"en-US": [{"sys": {"type": "Link", "linkType": "Asset", "id": message.media.id}}]}})

    new_entry = {"content_type_id": CONTENTFUL_WHATSAPP_TYPE, "fields": fields}

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


def upload_post_to_contentful(post: ContentfulPost):
    fields  = {
            "body": {"en-US": post.body},
            "title": {"en-US": post.title},
            "slug": {"en-US": post.slug},
            "publishDate": {"en-US": datetime.now().strftime(TIME_FORMAT)},
        }

    if len(post.media) > 0:
        media_list = []
        for media in post.media:
            media_list.append({"sys": {"type": "Link", "linkType": "Asset", "id": media.id}})

        fields.update({"media": {"en-US": media_list}})

    if post.cover:
        fields.update({"coverImage": {"sys": {"type": "Link", "linkType": "Asset", "id": post.cover[0].id}}})

    new_entry = {
        "content_type_id": CONTENTFUL_POST_TYPE,
        "fields": fields,
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
