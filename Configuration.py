import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'so powerfull secret key'
	DEBUG = True
	DATABASE = '/tmp/mainDB.db'