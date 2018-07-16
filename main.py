from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

import resources
import models


def create_app(script_info, test_config=None):
    # Flask's loader checks for script_info in the arguments and does some magic
    # Since we're not using it, just delete it to make linters happy
    del script_info

    app = Flask(__name__)

    # Load defaults
    app.config.from_pyfile('config/default.py')

    if not test_config:
        app.config.from_envvar('SFAA_SETTINGS')
    else:
        app.config.from_object(test_config)

    api = Api(app)

    models.db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedTokenModel.is_jti_blacklisted(jti)

    api.add_resource(resources.UserRegistration, '/registration')
    api.add_resource(resources.UserLogin, '/login')
    api.add_resource(resources.UserLogoutAccess, '/logout/access')
    api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/token/refresh')
    api.add_resource(resources.AllUsers, '/users')
    api.add_resource(resources.SecretResource, '/secret')
    api.add_resource(resources.UserEmailConfirmation, '/confirm/<string:token>', endpoint='user.confirm')

    @app.before_first_request
    def create_tables():
        models.db.create_all()

    @app.route("/")
    def hello():
        return jsonify({"hello": "World!"})

    return app
