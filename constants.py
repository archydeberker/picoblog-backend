import os

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

CONTENTFUL_TOKEN = os.environ.get("CONTENTFUL_TOKEN")
CONTENTFUL_SPACE_ID = os.environ.get("CONTENTFUL_SPACE_ID")

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

CONTENTFUL_WHATSAPP_TYPE = "whatsAppMessage"
CONTENTFUL_USER_TYPE = "user"
CONTENTFUL_POST_TYPE = "post"
TAG_REGEX = "#[A-Za-z]*\S"
CONTENTFUL_SPACE = "ykwd6jregaye"
CONTENTFUL_ENVIRONTMENT_ID = "master"
