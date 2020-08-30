import random
from datetime import datetime
from typing import List

import contentful_management
from contentful import Entry

from constants import CONTENTFUL_WHATSAPP_TYPE, CONTENTFUL_POST_TYPE, TIME_FORMAT
from models import WhatsAppMessage, Post

client = contentful_management.Client('CFPAT-JhmsGHABq620dFA4KsLlLvfinkhE8nKuSbhtvF5O0Fc')

space = 'ykwd6jregaye'
environment_id = 'master'
environment = client.environments(space).find(environment_id)


def generate_new_entry_id():
    return str(random.randint(1, 1000))


def upload_asset_to_contentful():
    pass


def get_all_unpublished_messages():
    messages = environment.entries().all()
    return [m for m in messages if m.content_type.id ==
            CONTENTFUL_WHATSAPP_TYPE and not m.is_archived]


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
        try:
            entry.archive()
        except:
            print('Failed to archive')


def upload_post_to_contentful(post: Post):
    new_entry = {
        "content_type_id": CONTENTFUL_POST_TYPE,
        "fields": {
            "body": {"en-US": post.body},
            "title": {'en-US': post.title}
        },
    }

    new_entry = environment.entries().create(generate_new_entry_id(), new_entry)

    new_entry.save()
    new_entry.publish()


if __name__ == '__main__':
    spaces = client.spaces().all()
    assets = client.assets(space, environment_id).all()
    print(assets)
    entries = client.entries(space, environment_id).all()
    most_recent = entries[0]
    print(most_recent)

