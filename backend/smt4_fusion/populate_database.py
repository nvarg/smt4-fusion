from .app import create_app
from .flask_extensions import db

def create_tables():
    app = create_app()
    db.create_all()
    return app, db
