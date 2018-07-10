from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256


db = SQLAlchemy()


class UserModel(db.Model):
    """User basic information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def save_to_db(self):
        """Save this object to the DB"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates the last-updated time and saves the changes"""
        self.updated = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        """Generate a secure password hash"""
        # TODO: This isn't secure! Use a better hash!
        return sha256.hash(password)

    def verify_password(self, plaintext):
        """Verify plaintext password matches hashed password in DB"""
        # TODO: This isn't secure! Use a better hash!
        return sha256.verify(plaintext, self.password)

    @classmethod
    def find_by_email(cls, email):
        """Lookup a user by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        """Helpful in debugging to return all users"""
        def to_json(x):
            return {
                'email': x.email,
                'password': x.password,
                'active': x.active,
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        """Helpful in debugging to reset the users table"""
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


class RevokedTokenModel(db.Model):
    """Revoked tokens, used in logout"""
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(128))
    # TODO: Cleanup or store in Redis to better deal with expired tokens

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
