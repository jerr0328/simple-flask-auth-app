from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

import resources
import models


def create_app():
    # TODO: Load configuration from file
    app = Flask(__name__)
    api = Api(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'some-secret-string'  # TODO: Change this!
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'  # TODO: Change this!
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

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
