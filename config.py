import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "gentleman don't change" ;
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True;

    @staticmethod
    def init_app(app):
        pass;

class DevelopmentConfig(Config):
    DEBUG = True;
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/myblog';

config = {'development':DevelopmentConfig,'default':DevelopmentConfig}
