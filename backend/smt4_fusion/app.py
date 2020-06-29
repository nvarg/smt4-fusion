import os
import sys
import logging
import argparse
from flask import Flask
from flask_cors import CORS

from .flask_extensions import db

from .api.demons import blueprint as demons_blueprint
from .api.images import blueprint as images_blueprint


def create_app():
    app = Flask(__name__.split('.')[-1])
    app.config.from_object('smt4_fusion.default_settings')
    if 'FLASK_CONFIG' in os.environ:
        app.config.from_envvar('FLASK_CONFIG')
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    CORS(app)
    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    db.create_all()


def register_blueprints(app):

    blueprints = [
        demons_blueprint,
        images_blueprint,
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
