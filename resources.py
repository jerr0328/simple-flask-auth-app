import logging

from flask import current_app, render_template, url_for
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from itsdangerous import URLSafeTimedSerializer

from models import UserModel, RevokedTokenModel
import emails

logger = logging.getLogger(__name__)


parser = reqparse.RequestParser()
parser.add_argument('email', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    """Handle User Registration"""
    def post(self):
        data = parser.parse_args()
        # TODO: Validate/sanitize email format

        if UserModel.find_by_email(data['email']):
            return {'message': "Email {} already exists".format(data['email'])}

        # Create the user, remember to hash the password!
        new_user = UserModel(
            email=data['email'],
            password=UserModel.generate_hash(data['password']),
            active=False
        )
        try:
            new_user.save_to_db()
        except:
            logger.exception("Error saving new user to DB")
            return {'message': "Something went wrong"}, 500

        try:
            # This email confirmation code mostly comes from:
            # https://github.com/MaxHalford/flask-boilerplate/blob/master/app/views/user.py

            # Serializer for generating random tokens
            ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

            # Subject of the confirmation email
            subject = 'Please confirm your email address.'
            # Generate a random token
            token = ts.dumps(new_user.email, salt='email-confirm-key')
            # Build a confirm link with token
            confirm_url = url_for('user.confirm', token=token, _external=True)
            # Render an HTML template to send by email
            html = render_template('email-confirm.html',
                                   confirm_url=confirm_url)
            # Send the email to user
            emails.send(new_user.email, subject, html)

            return {
                'message': 'User {} was created, please verify your email'.format(data['email']),
            }
        except:
            logger.exception("Something went wrong sending confirmation email")
            return {'message': "Something went wrong"}, 500


class UserEmailConfirmation(Resource):
    """Handle email confirmation response"""
    def get(self, token):
        """Yes, this shouldn't be a GET, but users clicking URLs will generate a GET"""
        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = ts.loads(token, salt='email-confirm-key')
            # TODO: set `max_age=86400` above and handle re-sending confirmation email
        # The token can either expire or be invalid
        except:
            return {'message': "Unknown email confirmation token"}, 404

        # Get the user from the database
        user = UserModel.find_by_email(email)
        user.active = True
        user.update()
        return {'message': "Email successfully confirmed! You can now login."}


class UserLogin(Resource):
    """Handle user login"""
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_email(data['email'])
        if not current_user:
            return {'message': "Email {} doesn't exist".format(data['email'])}, 401

        # Verify user is active
        if not current_user.active:
            return {'message': "Email {} is not yet verified".format(data['email'])}, 401

        # If the password matches, generate and send the token
        if current_user.verify_password(data['password']):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {
                'message': 'Logged in as {}'.format(current_user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': "Wrong credentials"}, 401


class UserLogoutAccess(Resource):
    """Handle logout with the JWT access token"""
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    """Handle logout with the JWT refresh token"""
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    """Refresh the access token with the JWT refresh token"""
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    """TODO: Remove before flight"""
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    """Sample secret, protected by JWT access token"""
    @jwt_required
    def get(self):
        return {'answer': 42}
