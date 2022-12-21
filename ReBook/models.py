from datetime import datetime
from ReBook import db, login_manager
from flask_login import UserMixin
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


favorite = db.Table('favorite',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('book_id', db.String(128), db.ForeignKey('book.id')),
	)

reading = db.Table('reading',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('book_id', db.String(128), db.ForeignKey('book.id')),
	db.Column('page', db.Integer, default=0),
	db.Column('last_read', db.DateTime, default=datetime.utcnow),
	db.Column('booked_date',  db.DateTime, default=datetime.utcnow)
	)

readend = db.Table('readend',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('book_id', db.String(128), db.ForeignKey('book.id')),
	)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	username = db.Column(db.String(128), nullable=False, unique=True)
	email = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.String(128), nullable=False)
	bio = db.Column(db.String(1024))
	image = db.Column(db.String(128), default="default.png")
	followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
	posts = db.relation('Post', backref='author', lazy=True)
	favorites = db.relation('Book', secondary=favorite, backref='fav_user')
	readings = db.relation('Book', secondary=reading, backref='reading_user')
	readends = db.relation('Book', secondary=readend, backref='readend_user')

	def __repr__(self):
		return "[{}] {} {}".format("User", self.id, self.username)


	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def follow_posts(self):

		page = request.args.get('page', 1, type=int)

		followed = Post.query.join(
			followers, (followers.c.followed_id == Post.user_id)).filter(
				followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.date_posted.desc()).paginate(page=page, per_page=25)

	def get_reset_token(self, expires_sec=180):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token).get('user_id', None)
			return User.query.get(user_id)
		except Exception as e:		
			return None

class Book(db.Model):
	id = db.Column(db.String(128), primary_key=True, nullable=False)
	title = db.Column(db.String(128))
	authors = db.Column(db.String(128))
	averageRating = db.Column(db.String(500))
	thumbnail = db.Column(db.String(500))
	pageCount = db.Column(db.Integer)

	def __repr__(self):
		return "[{}] {} {}".format("Book", self.id, self.title)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	title = db.Column(db.String(1024))
	content = db.Column(db.String(10000))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return "[{}] {} {}".format("Post", self.id, self.title)

