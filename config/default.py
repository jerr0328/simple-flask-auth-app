DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'some-secret-string'  # NOTE: Don't commit real secrets!
JWT_SECRET_KEY = 'jwt-secret-string'  # NOTE: Don't commit real secrets!
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']