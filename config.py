import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'book.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = 'AIzaSyCccg9U1mS1FGOM21m8FFOdz7JL6zaidLQ'
