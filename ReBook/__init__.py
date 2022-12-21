from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from ReBook.config import Config

<<<<<<< HEAD
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '7bd027b66da4d3a02c91b2396617a02a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://shupi:Dureti@localhost/rebook'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
=======
>>>>>>> f64ff04 (blueprint)

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.Login'

def create_app(config_class=Config):

	app = Flask(__name__, static_url_path='/static')
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from ReBook.users.routes import users
	from ReBook.posts.routes import posts
	from ReBook.books.routes import books
	from ReBook.main.routes import main
	from ReBook.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(books)
	app.register_blueprint(errors)

	return app

