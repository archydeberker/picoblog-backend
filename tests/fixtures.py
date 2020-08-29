import pytest
import os

import models
from app_factory import create_app
from config import TestConfig
from models import db


@pytest.fixture(scope='session')
def setup_test_app():

    app = create_app(config=TestConfig)
    app.app_context().push()

    # Note that we do this for tests, when each DB is created from scratch, but we don't do it for prod, when the
    # DB is incrementally updated via alembic
    db.create_all()

    with app.test_client() as client:
        yield client, db, app

    print('Removing Test DB')
    try:
        os.remove(TestConfig.db_filepath)  # this is teardown
    except FileNotFoundError:
        Warning('Did not manage to tear down test DB, hope this was a temporary env')


@pytest.fixture(scope="module")
def test_db(setup_test_app):
    _, db, _ = setup_test_app

    yield db


@pytest.fixture(scope="module")
def populate_test_db(test_db):
    user = models.User(number='1234')
    assert user.number is '1234'

    db.session.add(user)
    db.session.commit()


