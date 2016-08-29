# -*- coding: utf-8 -*-


"""Application configuration."""


# Python standard libraries
import os


class Config(object):
    """Base configuration."""

    DEBUG = False
    TESTING = False
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = str(os.environ['DATABASE_URL'])
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 12


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    TESTING = False
    CACHE_TYPE = 'simple'
    BCRYPT_LOG_ROUNDS = 4


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'
    TESTING = True
    DEBUG = True
    CACHE_TYPE = 'simple'
    BCRYPT_LOG_ROUNDS = 4

