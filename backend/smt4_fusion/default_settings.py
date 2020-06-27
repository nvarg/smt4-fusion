from os import environ

DEBUG = False
TESTING = False
SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///:memory:')
ITEMS_PER_PAGE = environ.get('ITEMS_PER_PAGE', 5)
