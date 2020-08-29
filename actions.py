import models
import re

from datetime import datetime
from contentful_utils import client

def get_or_create(model, session=models.db.session, **kwargs):
    """
    Retrieve item from the DB, create it if it doesn't exist already.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def store_new_message(message_form):
    print(message_form)

    user = get_or_create(models.User, number=message_form['From'])
    body = message_form['Body']

    body, tags = parse_message(body)
    msg = models.Message(body=body,
                         user=user,
                         sent=datetime.now(),
                         received=datetime.now(),
                         tags=tags)

    models.db.add(msg)
    models.db.commit()

    # As an experiment, we'll also add it to contentful
    new_entry = {'content_type_id': 'whatsAppMessage',
                 'fields': dict(body=body, from=message_form['From'], timestamp_received=datetime.now())}}

def parse_message(message):
    """

    :param message: text of a whatsapp message
    :return:
    """

    tags = [t for t in message.split() if '#' in t]
    body = [t for t in message.split() if '#' not in t]

    tag_list = []
    for tag in tags:
        tag_list.append(get_or_create(models.Tag, value=tag))

    return body, tags

