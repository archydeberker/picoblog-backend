from flask import Flask
from flask_migrate import Migrate
from flask_graphql import GraphQLView

from config import Config
from models import db
from graph import schema
from routes import api


def create_app(db=db, config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    print(f"Using database at {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.register_blueprint(api)
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
    )

    app.app_context().push()

    db.init_app(app)
    db.session.commit()

    Migrate(app, db)

    return app
