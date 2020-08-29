import json

from flask import Blueprint, request
from actions import store_new_message

api = Blueprint("api", __name__)


@api.route("/api/message", methods=["GET", "POST"])
def new_message():
    msg = request.form
    store_new_message(msg)
    return json.dumps("Message Received")


