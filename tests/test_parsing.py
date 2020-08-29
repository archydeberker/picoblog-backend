import actions
from tests.fixtures import test_db, setup_test_app


def test_tag_parsing(test_db):
    test_message = '#title My Great Adventure'
    body, tags = actions.parse_message(test_message)
    assert '#title' in tags
