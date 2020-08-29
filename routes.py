from flask import Blueprint, request

api = Blueprint("api", __name__)


@api.route("/api/message", methods=["GET", "POST"])
def new_message():
    msg = request.get_json()
    return "Message Received"
