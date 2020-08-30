from contentful_management import Entry

import constants

import re

from dataclasses import dataclass
from typing import List
import random

def remove_hashtags(text):
    return re.sub(constants.TAG_REGEX, '', text)


def find_hashtags(text):
    return [tag.strip() for tag in re.findall(constants.TAG_REGEX, text)]


def contentful_to_dict(entry):
    return {'Body': entry.body,
            'From': None}


@dataclass
class WhatsAppMessage:
    raw: dict

    def __post_init__(self):
        self.body = self.raw['Body']
        self.tags = find_hashtags(self.raw['Body'])
        self.sender = self.raw['From']

        if int(self.raw['NumMedia']) > 0:
            # I haven't managed to send multiple files combined yet, not sure why
            # Any media items are available from Twilio at this URL
            self.media = Media(url=self.raw.get('MediaUrl0'),
                               content_type=self.raw.get('MediaContentType0'),
                               title= self.raw.get('MediaUrl0').split('/')[-1],
                               owner=self.sender)
        else:
            self.media = None

    @property
    def publish(self):
        return "#publish" in self.tags

    @property
    def assets(self):
        return None

    @property
    def title(self):
        return '#title' in self.tags


@dataclass
class Post:
    messages: List[WhatsAppMessage]

    def __post_init__(self):
        self.body = '\n \n'.join([remove_hashtags(m.body) for m in self.messages])

    @property
    def title(self):
        """
        Find the latest message which included #title and use that.
        """
        for message in self.messages:
            if message.title:
                return remove_hashtags(message.body)

        return f'Post {random.randint(0, 100000)}'

    @property
    def slug(self):
        return self.title.lower().replace(' ', '-')


@dataclass
class Media:
    url: str
    content_type: str
    title: str
    owner: str

