from graphene.test import Client
from graph import schema
from tests.fixtures import setup_test_app, test_db, populate_test_db


def test_basic_query(populate_test_db):
    client = Client(schema)
    executed = client.execute("""{users {number, id }}""")
    assert executed == {"data": {"users": [{"id": "1", "number": "1234"}]}}
