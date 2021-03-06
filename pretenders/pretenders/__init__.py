import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from routes.ping import ping_blueprint
    from routes.users import users_blueprint
    from routes.contests import contests_blueprint
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(contests_blueprint)


    return app
