from contentful_management import Entry

import constants

import re

from dataclasses import dataclass
from typing import List, Union
import random


def remove_hashtags(text):
    return re.sub(constants.TAG_REGEX, "", text)


def find_hashtags(text):
    return [tag.strip().lower() for tag in re.findall(constants.TAG_REGEX, text)]


def contentful_entry_to_class(entry):

    # Convert media fields
    content_dict = entry.fields()
    media = content_dict.get('media')
    if media is not None:
        # Only support a single entry for now
        media = ContentfulMedia(id=media[0].id)

    return ContentfulWhatsAppMessage(body=content_dict['body'],
                                     user=ContentfulUser(number=content_dict['user'].id,
                                                         name=content_dict['user'].id),
                                     media=media)


@dataclass
class TwilioMedia:
    url: str
    content_type: str
    title: str
    owner: str


@dataclass
class ContentfulMedia:
    id: str


@dataclass
class ContentfulUser:
    number: str
    name: str=None

    @property
    def id(self):
        return self.number


@dataclass
class TwilioWhatsAppMessage:
    raw: dict

    def __post_init__(self):
        self.body = self.raw["Body"]
        self.tags = find_hashtags(self.raw["Body"])
        self.sender = self.raw["From"]

        num_media = self.raw.get("NumMedia") or 0
        if int(num_media) > 0:
            # I haven't managed to send multiple files combined yet, not sure why
            self.media = TwilioMedia(
                url=self.raw.get("MediaUrl0"),
                content_type=self.raw.get("MediaContentType0"),
                title=self.raw.get("MediaUrl0").split("/")[-1],
                owner=self.sender,
            )
        else:
            self.media = None

    @property
    def publish(self):
        return "#publish" in self.tags

    @property
    def name(self):
        return "#name" in self.tags

    @property
    def location(self):
        return "#location" in self.tags

    @property
    def assets(self):
        return None

    @property
    def title(self):
        return "#title" in self.tags


@dataclass
class ContentfulWhatsAppMessage:
    body: str
    media: Union[ContentfulMedia, None]
    user: ContentfulUser

    def __post_init__(self):
        self.tags = find_hashtags(self.body)

    @property
    def title(self):
        return "#title" in self.tags


@dataclass
class ContentfulPost:
    messages: List[ContentfulWhatsAppMessage]

    def __post_init__(self):
        self.body = "\n \n".join([m.body for m in reversed(self.messages) if not m.title])

    @property
    def title(self):
        """
        Find the latest message which included #title and use that.
        """
        for message in self.messages:
            if message.title:
                return remove_hashtags(message.body)

        return f"Post {random.randint(0, 100000)}"

    @property
    def slug(self):
        return self.title.lower().replace(" ", "-")

    @property
    def media(self):
        return [m.media for m in self.messages if m.media]

    @property
    def cover(self):
        return [m.media for m in self.messages if "#coverimage" in m.tags] or None

    @property
    def user(self):
        return self.messages[0].user