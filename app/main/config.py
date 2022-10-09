import os

# uncomment the line below for postgres database url from environment variable
db_conn = os.environ['DATABASE_URL']


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = True



class DevelopmentConfig(Config):
    #https://flask.palletsprojects.com/en/2.2.x/config/
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = db_conn
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_db_test.db')
    SQLALCHEMY_DATABASE_URI = db_conn
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = db_conn


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
