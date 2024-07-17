import os
class Config:
    SECRET_KEY = 'b805fca3e1f0d79cb3e3972864137fc6'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\abc\\Desktop\\Python\\virtualenv\\flask_project\\site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = 'eoix obzi jfgq hhau'