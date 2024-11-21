import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ed668c94f7a91c8b')  
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'haukong1308@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'pbbn mdtj ganl pruj')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
