import json

from flask import Blueprint, request
from actions import handle_new_message

api = Blueprint("api", __name__)


@api.route("/api/message", methods=["GET", "POST"])
def new_message():
    msg = request.form
    print(msg)
    handle_new_message(msg)
    return json.dumps("Message Received")


