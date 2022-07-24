import os
basedir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(basedir, 'data')
if not os.path.exists(datadir):
    os.mkdir(datadir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'beefcake'
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(datadir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_LIFESPAN = {'minutes': 30}
    JWT_REFRESH_LIFESPAN = {'days': 30}

    SECURITY_CHANGEABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or '146585145368132736173505678016728509634'
    SECURITY_RECOVERABLE = True

    SEND_REGISTER_EMAIL = True
    MAIL_USERNAME = "AKIAYRYXROWHHUZF6WU4"
    MAIL_PASSWORD = "BLiMR8GARzhowengFGvMKAhG/SJCY21ERahRJr4dR8V3"
    MAIL_SERVER = "email-smtp.us-east-2.amazonaws.com"
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_DEFAULT_SENDER = "evancarr53@gmail.com"


