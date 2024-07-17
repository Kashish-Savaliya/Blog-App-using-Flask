from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config
import os
import socket

socket.getaddrinfo('localhost', 8080)

db=SQLAlchemy()
login_manager = LoginManager()
# if user is not logged in and tries to access the account page
# then it redirects to login page using this login_view
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # bcrypt = Bcrypt(app)
    with app.app_context():
        db.create_all()

    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app

app = create_app()


# print(type(app.config['SECRET_KEY'] ))
