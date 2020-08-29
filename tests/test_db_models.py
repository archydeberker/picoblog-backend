import datetime

import models
from models import db

from tests.fixtures import test_db, setup_test_app


number = '122323'


class TestInsertion:

    def test_user_can_be_added(self, test_db):
        user = models.User(number=number)
        assert user.number is number

        db.session.add(user)
        db.session.commit()

    def test_addition_of_tags(self, test_db):

        tags = ['title', 'body', 'caption']
        for t in tags:
            tag = models.Tag(value=t)
            db.session.add(tag)

        db.session.commit()

    def test_addition_of_messages(self, test_db):

        for body, tag in zip(['Test 1', 'Test 2', 'Test 3'],
                              ['title', 'body', 'caption']):
            msg = models.Message(body=body,
                             tags=[models.Tag(value=tag)],
                             post=models.Post(created=datetime.datetime.now()),
                             user_number=number,
                             sent=datetime.datetime.now(),
                             received=datetime.datetime.now())

            db.session.add(msg)

        db.session.commit()

    def test_addition_of_messages_to_post(self):
        post = models.Post.query.filter_by(id=1).first()
        msg = models.Message(body='Test 4',
                             post=post,
                             user_number=number,
                             sent=datetime.datetime.now(),
                             received=datetime.datetime.now())

        db.session.add(msg)
        db.session.commit()

        assert msg.post.id == 1


class TestRetrieval:

    def test_query_messages_for_user(self, test_db):
        user = models.User.query.filter_by(number=number).first()

        assert len(user.messages) is 4

    def test_messages_assigned_to_correct_post(self, test_db):
        messages = models.Message.query.limit(4).all()
        for i, m in enumerate(messages[:3]):
            assert m.post.id == i + 1

        assert messages[-1].post.id == 1

    def test_retrieve_messages_for_post(self):
        posts = models.Post.query.limit(3)
        for p in posts:
            assert len(p.messages) >= 1

