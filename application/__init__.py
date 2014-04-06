# -*- coding: utf-8 -*-
"""
    flaskage.application
    ~~~~~~~~~~~~~~~~~~~~

    This module initialises all required Flask extensions and provides
    the create_app using application factory function.  See the page at
    http://flask.pocoo.org/docs/patterns/appfactories/ for further details
    relating to Flask application factories.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.assets import Environment
from flask.ext.login import LoginManager

from config import AVAILABLE_CONFIGS

db = SQLAlchemy()
migrate = Migrate()
assets = Environment()
login_manager = LoginManager()


def create_app(config):

    # Create and configure the Flash application
    app = Flask(__name__)
    app.config.from_object(AVAILABLE_CONFIGS[config])

    # Initialise Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    assets.init_app(app)
    login_manager.init_app(app)

    # Initialise Jinja2 extensions
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    app.jinja_env.pyjade.options['autocloseCode'] = ['assets']

    # Provide the Flask-Login user loader function
    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(id)

    # Setup app logging if necessary
    # app.logger.setLevel(logging.INFO)

    # Setup app hooks if necessary
    # @app.before_request
    # def before_request():
    #     pass

    # Setup app error handlers if necessary
    # @app.errorhandler(403)
    # def forbidden(error):
    #     return render_template("403.html"), 403

    # @app.errorhandler(404)
    # def not_found(error):
    #     return render_template("404.html"), 404

    # @app.errorhandler(500)
    # def internal_server_error(error):
    #     return render_template("500.html"), 500

    # Import and register Blueprints
    from .views import flaskage
    # from .views import module1
    # from .views import module2
    app.register_blueprint(flaskage.mod)
    # app.register_blueprint(module1.mod)
    # app.register_blueprint(module2.mod)

    return app
