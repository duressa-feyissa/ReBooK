import os


class Config:
	SECRET_KEY = '7bd027b66da4d3a02c91b2396617a02a'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///rebook.db'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.getenv("EMAIL", None)
	MAIL_PASSWORD = os.getenv("PASS", None)
	
