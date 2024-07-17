from datetime import datetime
from flask_blog import db,login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
import logging
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20) , unique=True, nullable=False)
    # username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False ,default='default.jpeg')
    password = db.Column(db.String(60),nullable=False)
    #Creating a one-to-many relationship i.e 1 user many posts
    ''' backref is similar to adding another column to post model,what
        backref allow us to do is when we have a post ,the author attribute allow us
        to get the user who created the post
        The lazy attribute defines when SQlAlchemy loads the data from the database
        ,so true means that SQlAlchemy will load the data as necessary in one go '''

    posts = db.relationship('Post', backref='author', lazy=True)

    # Create a token
    def get_reset_token(self,expires_sec=1800):
        # uses the Serializer class to serialize the user's ID along with a secret key to create a token.
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        # Creating a token. The user's ID is passed into the token payload.
        # This calls the dumps method of the Serializer object (s) with the dictionary {'user_id': self.id} as an argument.
        # The dumps method serializes the dictionary into a token. The resulting token is a string representation of the dictionary data,
        # encoded in a way that can be safely transmitted or stored.
        token = s.dumps({'user_id': self.id})
        # This line encodes the token into a UTF-8 encoded byte string.
        encoded_token = token.encode('utf-8')
        # This line decodes the UTF-8 encoded byte string back into a Unicode string.
        decoded_token = encoded_token.decode('utf-8')
        # This line returns the decoded token, which is now in a string format.
        return decoded_token

    # Verifies a token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # print("hello")
            # s.loads(token) -> This calls the loads method of the Serializer object (s) with the token as an argument.
            # The loads method deserializes the token, meaning it reverses the serialization process that was used to create the token.
            # It returns a Python dictionary containing the data that was stored in the token.
            print("Token:", token)
            data = s.loads(token)
            # ['user_id'] -> This accesses the value corresponding to the key 'user_id' in the dictionary returned by s.loads(token).
            # This key-value pair was added to the token during the serialization process to store the user's ID.
            print("Decoded data:", data)
            user_id = data.get('user_id')
            # print(user_id)

            if user_id is not None:
                # Query the database for the user with the extracted user ID
                user = User.query.get(user_id)
                # Return the user object
                return user
            else:
                # If user ID is None, return None
                return None
        except Exception as e:
                # Handle the exception and print its details
            print("An exception occurred:", str(e))
            return None
        # return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}' ,'{self.date_posted}')"
