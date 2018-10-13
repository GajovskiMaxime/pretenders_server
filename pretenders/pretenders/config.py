import os  # new


class BaseConfig:
    """Base configuration"""
    SECRET_KEY = 'my_precious'
    TESTING = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')