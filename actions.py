import contentful_utils
from messages import Onboarding
from models import TwilioWhatsAppMessage, ContentfulPost, contentful_entry_to_class, ContentfulUser


def extract_assets(message_dict):
    pass


def build_and_publish_post():
    """
    Fetch all unpublished messages from Contentful, compile them into a blogpost, and publish.

    :return:
    """
    messages = contentful_utils.get_all_unpublished_messages()
    if len(messages) is 0:
        print("Aborting, no new messages")
        return []

    new_messages = [contentful_entry_to_class(m) for m in messages]

    post = ContentfulPost(messages=new_messages)

    contentful_utils.upload_post_to_contentful(post)

    return messages


def handle_triggers(message):

    if message.publish:
        print("Found publish trigger")
        included_messages = build_and_publish_post()
        contentful_utils.archive_messages(included_messages)


def get_response(user):

    if user.name is None:
        return Onboarding.need_name
    if user.location is None:
        return Onboarding.need_location
    else:
        return None


def send_reply(text, user: ContentfulUser):
    pass

def handle_new_message(message_dict):
    """

    Processes a new message, storing it in Contentful and triggering any other necessary actions.

    :param message_dict:
    :return:

    """

    message = TwilioWhatsAppMessage(message_dict)

    user = contentful_utils.find_user(message.sender)

    if user is None:
        print('No user found, creating a new one')
        user = contentful_utils.create_user(message.sender)
        send_reply(Onboarding.need_name, user)

    if message.name:
        contentful_utils.add_name_to_user(message, user)
        send_reply(Onboarding.need_location, user)

    if message.location:
        contentful_utils.add_location_to_user(message, user)
        send_reply(Onboarding.onboarding_complete, user)

    if message.publish:
        handle_triggers(message)
    else:
        if message.media:
            asset_id = contentful_utils.upload_assets_to_contentful(message.media, user)
            message.media.id = asset_id
        contentful_utils.upload_message_to_contentful(message)
