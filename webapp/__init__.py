from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.bcrypt import Bcrypt
from flask.ext.assets import Environment

from config import AVAILABLE_CONFIGS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
assets = Environment()


def create_app(config):

    # Create and configure the Flash application
    app = Flask(__name__)
    app.config.from_object(AVAILABLE_CONFIGS[config])

    # Initialise all Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    assets.init_app(app)

    # Little workaround to allow custom asset load path
    # https://github.com/miracle2k/flask-assets/issues/35
    assets.url = app.static_url_path

    # Setup app logging if necessary
    # app.logger.setLevel(logging.INFO)

    # Setup app hooks if necessary
    # @app.before_request
    # def before_request():
    #     pass

    # Setup app error handlers if necessary
    # @app.errorhandler(404)
    # def not_found(error):
    #     return render_template("404.html"), 404

    # Import and register Blueprints
    # from .views import module1
    # from .views import module2
    # app.register_blueprint(module1.mod)
    # app.register_blueprint(module2.mod)

    return app
