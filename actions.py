import contentful_utils
from models import WhatsAppMessage, Post, contentful_to_dict


def extract_assets(message_dict):
    pass


def build_and_publish_post():
    """
    Fetch all unpublished messages from Contentful, compile them into a blogpost, and publish.

    :return:
    """
    new_messages = contentful_utils.get_all_unpublished_messages()
    new_messages = [WhatsAppMessage(contentful_to_dict(m)) for m in new_messages]

    post = Post(messages=new_messages)
    contentful_utils.upload_post_to_contentful(post)


def handle_new_message(message_dict):
    """

    Processes a new message, storing it in Contentful and triggering any other necessary actions.

    :param message_dict:
    :return:

    """

    message = WhatsAppMessage(message_dict)
    if message.publish:
        build_and_publish_post()
    else:
        contentful_utils.upload_message_to_contentful(message)



