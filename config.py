import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'IMAGETRAVELLERDABEST'
    # we dont use SQLALCHEMY BUT IF WE DO
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # WE DONT USE MAIL AS WELL
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SKIP ALL THE MAILS AND DATABASE STUFF

class TestingConfig(Config):
    TESTING = True
    # Skipping the database config

class ProductionConfig(Config):
    # SKIPPING THE Database again
    pass

config = {
    'development' : DevelopmentConfig,
    'testing'     : TestingConfig,
    'production'  : ProductionConfig,

    'default'     : DevelopmentConfig
}
