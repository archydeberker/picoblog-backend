from flask import Flask

from config import Config
from routes import api


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(api)

    app.app_context().push()

    return app
