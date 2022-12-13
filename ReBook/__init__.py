from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '7bd027b66da4d3a02c91b2396617a02a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://shupi:Dureti@localhost/rebook'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'Login'

from ReBook import route
