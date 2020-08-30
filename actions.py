import contentful_utils
from models import WhatsAppMessage, Post, contentful_to_dict


def extract_assets(message_dict):
    pass


def build_and_publish_post():
    """
    Fetch all unpublished messages from Contentful, compile them into a blogpost, and publish.

    :return:
    """
    messages = contentful_utils.get_all_unpublished_messages()
    if len(messages) is 0:
        print('Aborting, no new messages')
        return []

    new_messages = [WhatsAppMessage(contentful_to_dict(m)) for m in messages]

    post = Post(messages=new_messages)

    contentful_utils.upload_post_to_contentful(post)

    return messages


def handle_new_message(message_dict):
    """

    Processes a new message, storing it in Contentful and triggering any other necessary actions.

    :param message_dict:
    :return:

    """

    message = WhatsAppMessage(message_dict)
    if message.publish:
        print('Found publish trigger')
        included_messages = build_and_publish_post()
        contentful_utils.archive_messages(included_messages)
    else:
        contentful_utils.upload_assets_to_contentful(message)
        contentful_utils.upload_message_to_contentful(message)

