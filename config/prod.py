import os

"""Production settings that should be passed from the environment"""


def get_env(name, required=True):
    """
    Get value from environment
    :param name: Environment variable name
    :param required: True to raise exception if key is missing
    :return: Environment variable value
    """
    val = os.getenv(name)
    if required and not val:
        raise ValueError("No {} set for Flask application".format(name))


SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = get_env('SECRET_KEY')
JWT_SECRET_KEY = get_env('JWT_SECRET_KEY')
DEBUG = False
TESTING = False
