import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/'
    REDIS_DATABASE_ID = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
