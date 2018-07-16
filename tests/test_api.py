from main import create_app
from models import db, UserModel
from flask_testing import TestCase
import json

EMAIL = "test@test.com"
PASSWORD = "hunter2"
PAYLOAD = {"email": EMAIL, "password": PASSWORD}


class ApiTest(TestCase):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    def create_app(self):
        return create_app(None, self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def client_post(self, endpoint, payload):
        return self.client.post(endpoint, data=json.dumps(payload), content_type='application/json')

    def test_root(self):
        """Test sanity of app with simple request"""
        response = self.client.get('/')
        self.assertEquals(response.json, dict(hello='World!'))

    def test_user_registration(self):
        """Test correct user registration"""

        response = self.client_post('/registration', PAYLOAD)

        self.assertEqual(response.json, {'message': "User {} was created, please verify your email".format(EMAIL)})
        user = UserModel.find_by_email(EMAIL)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, EMAIL)
        # Ensure plaintext password is not stored
        self.assertNotEqual(user.password, PASSWORD)
        self.assertFalse(user.active)

    def test_duplicate_registration(self):
        """Test registration on existing email"""
        hashed_pass = UserModel.generate_hash('pass123')
        user = UserModel(
            email=EMAIL,
            password=hashed_pass,
            active=True,
        )
        user.save_to_db()

        response = self.client_post('/registration', PAYLOAD)

        self.assertEqual(response.json, {'message': "Email {} already exists".format(EMAIL)})
        user = UserModel.find_by_email(EMAIL)
        # Ensure user wasn't changed
        self.assertEqual(user.password, hashed_pass)

    def test_secret_no_login(self):
        """Test secret prevents non-logged in requests"""
        response = self.client.get('/secret')
        self.assert401(response)

    def test_login(self):
        """Test normal login with active user"""

        user = UserModel(
            email=EMAIL,
            password=UserModel.generate_hash(PASSWORD),
            active=True,
        )
        user.save_to_db()

        response = self.client_post('/login', PAYLOAD)
        self.assertIn('message', response.json)
        self.assertIn('access_token', response.json)
        self.assertIn('refresh_token', response.json)
        self.assertEqual(response.json['message'], 'Logged in as {}'.format(EMAIL))
        access_token = response.json['access_token']
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        secret_response = self.client.get('/secret', headers=headers)
        self.assert200(secret_response)
        self.assertEqual(secret_response.json, {'answer': 42})

    def test_login_attempt_wrong_user(self):
        """Test login attempt with non-existent user"""
        response = self.client_post('/login', PAYLOAD)

        self.assert401(response)
        self.assertEqual(response.json, {'message': "Email {} doesn't exist".format(EMAIL)})

    def test_login_attempt_wrong_password(self):
        """Test login attempt with existing user, wrong password"""
        user = UserModel(
            email=EMAIL,
            password=UserModel.generate_hash(PASSWORD),
            active=True,
        )
        user.save_to_db()

        payload = {'email': EMAIL, 'password': 'password'}
        response = self.client_post('/login', payload)

        self.assert401(response)
        self.assertEqual(response.json, {'message': "Wrong credentials"})

    def test_login_attempt_inactive(self):
        """Test login attempt with inactive (unverified) user"""
        user = UserModel(
            email=EMAIL,
            password=UserModel.generate_hash(PASSWORD),
            active=False,
        )
        user.save_to_db()

        response = self.client_post('/login', PAYLOAD)

        self.assert401(response)
        self.assertEqual(response.json, {'message': "Email {} is not yet verified".format(EMAIL)})


