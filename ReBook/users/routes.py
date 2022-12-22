from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from flask import render_template, request, jsonify, flash, redirect, url_for, Blueprint, current_app
from ReBook import bcrypt, db, mail
from ReBook.users.forms import RegistrationForm, Search, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from ReBook.models import User, Post
from flask_login import current_user, logout_user, login_required, login_user
from PIL import Image
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from uuid import uuid4
import os


users = Blueprint('users', __name__)


def send_verification_email(user_dictionary, expires_sec=180):
	s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
	token = s.dumps(user_dictionary).decode('utf-8')
	msg = Message('Email Verification', sender=os.getenv("EMAIL", None),
		recipients=[user_dictionary['email']])
	msg.body = f"""

	To verify your account, visit the following link:
	{url_for('users.verify_password', token=token, _external=True)}

	If you did not make this request then simply ignore this email!
	"""
	mail.send(msg)


@users.route('/register', methods=['GET', 'POST'])
def Register():

	if current_user.is_authenticated:
		return redirect(url_for('users.mainRoute'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user_dictionary = {'username': form.username.data, 'email': form.email.data, 'password': hashed_pass}
		send_verification_email(user_dictionary)
		flash(f'An email has been sent to verify your account! \nVerify your account in three minute to access your account!', 'success')
		return redirect(url_for('users.Login'))
	else:
		print("error")	
	return render_template('register.html', form=form)


@users.route("/verify/email/<token>")
def verify_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.mainRoute'))
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		username = s.loads(token).get('username', None)
		email = s.loads(token).get('email', None)
		password = s.loads(token).get('password', None)	
		user = User(username=username, email=email, password=password)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created successful!', 'success')
		return redirect(url_for('users.Login'))
	except Exception as e:
		flash("Your account hasn't been verified!", "warning")
		return redirect(url_for('users.Register'))


@users.route('/login', methods=['GET', 'POST'])
def Login():

	if current_user.is_authenticated:
		return redirect(url_for('main.mainRoute'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.mainRoute'))
		else:
			flash(f'Login Unsuccessful!', 'danger')
	return render_template('login.html', form=form)


@users.route('/logout')
def Logout():
	logout_user()
	return redirect(url_for('main.mainRoute'))


def save_file_name(name):
	extention = name.rsplit('.', 1)[1].lower()
	return str(uuid4()) + "." + extention 


@users.route('/account', methods=["GET", "POST"])
@login_required
def Account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			f = form.picture.data
			f.filename = save_file_name(f.filename)
			filename = secure_filename(f.filename)
			current_user.image = filename
			pic_path = os.path.join(current_app.root_path, 'static/images', filename)
			output_size = (125, 125)
			i = Image.open(f)
			i.thumbnail(output_size)
			i.save(pic_path)
		current_user.username = form.username.data
		current_user.bio = form.bio.data
		db.session.commit()
		return redirect(url_for('users.Account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.bio.data = current_user.bio
	image_file = url_for('static', filename='images/' + current_user.image)
	return render_template('account.html', form=form, image=image_file)


@users.route("/search", methods=['GET', 'POST'])
@login_required
def Searcher():
	image_file = url_for('static', filename='images/' + current_user.image)
	users=[]
	form = Search()
	if form.validate_on_submit():
		users = User.query.filter(User.username.like("%"+form.search.data+"%")).all()
		return render_template("search.html", image=image_file, form=form, time=datetime.utcnow(), users=users)
	return render_template("search.html", image=image_file, form=form, time=datetime.utcnow(), users=users)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
		sender=os.getenv("EMAIL", None),
		recipients=[user.email]
		)
	msg.body = f"""
	To reset your password, visit the following link:
	{url_for('users.reset_password', token=token, _external=True)}

	If you did not make this request then simply ignore this email and no change to it.
	"""

	mail.send(msg)


@users.route("/reset/request", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.mainRoute'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent to reset your password! \nReset your password in three minute!', 'info')
		return redirect(url_for('users.Login'))
	return render_template("reset_request.html", form=form)


@users.route("/reset/password/<token>", methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.mainRoute'))
	user = User.verify_reset_token(token)
	if user is None:
		flash("That is an expired token!", "warning")
		return redirect(url_for('users.Login'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pass
		db.session.commit()
		flash(f'Your password has been update!', 'success')
		return redirect(url_for('users.Login'))
	return render_template('reset_token.html', form=form)


@users.route("/user/<string:username>")
@login_required
def User_Posts(username):
	image_file = url_for('static', filename='images/' + current_user.image)
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(
		Post.date_posted.desc()).paginate(page=page, per_page=8)
	return render_template('user_post.html', posts=posts, image=image_file, user=user)


@users.route('/user/<int:user_id>')
@login_required
def Users(user_id):
	page = request.args.get('page', 1, type=int)
	user = User.query.get_or_404(user_id)
	image_file = url_for('static', filename='images/' + current_user.image)
	following, followers, flag = 0, 0, 0
	for u in user.followed:
		following+=1
	for u in user.followers:
		if u.id == current_user.id:
			flag = 1
		followers+=1

	user_followed = user.followed.paginate(per_page=20, page=page)

	return render_template('user.html', image=image_file, 
		following=following, user=user, followers=followers, flag=flag,
		user_followed=user_followed)


@users.route('/follow', methods=['POST'])
@login_required
def User_follow():
	res = request.form
	user_id = res['follow']
	user = User.query.filter_by(id=user_id).first()
	if user:
		current_user.follow(user)
		db.session.commit()
		return	jsonify({'data': "Success"})
	return jsonify({'data': 'failure'})


@users.route('/unfollow', methods=['POST'])
@login_required
def User_unfollow():
	res = request.form
	user_id = res['unfollow']
	user = User.query.filter_by(id=user_id).first()
	if user:
		current_user.unfollow(user)
		db.session.commit()
		return	jsonify({'data': "Success"})
	return jsonify({'data': 'failure'})
