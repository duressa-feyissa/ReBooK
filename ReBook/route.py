from datetime import datetime
from sqlalchemy import text
from flask import render_template, request, jsonify, flash, redirect, url_for, request
from ReBook import app, bcrypt, db
from ReBook.form import RegistrationForm, LoginForm, UpdateAccountForm, MakePost
from ReBook.models import User, Book, Post
from ReBook.parse import parse
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import os
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from uuid import uuid4


@app.route('/home')
@app.route('/')
def mainRoute():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('layout.html', image=image_file)
	return render_template('layout.html')
	
@app.route('/advanced')
def advancedRoute():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('advanced.html', image=image_file)
	return render_template('advanced.html')

@app.route('/book')
def bookRoute():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('view.html', image=image_file)
	return render_template('view.html')

@app.route('/process', methods=['POST'])
def process():
	res = request.form
	data = parse(res)
	return jsonify(data)

@app.route('/register', methods=['GET', 'POST'])
def Register():

	if current_user.is_authenticated:
		return redirect(url_for('mainRoute'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created successful!', 'success')
		return redirect(url_for('Login'))
	else:
		print("error")	
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def Login():

	if current_user.is_authenticated:
		return redirect(url_for('mainRoute'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('mainRoute'))
		else:
			flash(f'Login Unsuccessful!', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def Logout():
	logout_user()
	return redirect(url_for('mainRoute'))

def save_file_name(name):
	extention = name.rsplit('.', 1)[1].lower()
	return str(uuid4()) + "." + extention 

@app.route('/account', methods=["GET", "POST"])
@login_required
def Account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			f = form.picture.data
			f.filename = save_file_name(f.filename)
			filename = secure_filename(f.filename)
			current_user.image = filename
			pic_path = os.path.join(app.root_path, 'static/images', filename)
			output_size = (125, 125)
			i = Image.open(f)
			i.thumbnail(output_size)
			i.save(pic_path)
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('Account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='images/' + current_user.image)
	return render_template('account.html', title="Account", form=form, image=image_file)	

@app.route('/save', methods=["GET", "POST"])
@login_required
def Save():
	res = request.form
	check = Book.query.filter_by(id=res['id']).first()
	num = res['pageCount']
	hold = 0
	if num.isdigit():
		hold = int(num)
	else:
		hold = 1
	if check:
		flag = 0
		for read in current_user.readings:
			if check.id == read.id:
				flag = 1
				break
		if flag == 1:
			return jsonify({"data": "Already Saved"})
		else:
			current_user.readings.append(check)
			db.session.commit()
			return jsonify({"data": "Saved"})
	else:
		book = Book(id=res['id'], title=res['title'], authors=res['authors'],
		averageRating=res['averageRating'], thumbnail=res['thumbnail'], pageCount=hold)
		current_user.readings.append(book)
		db.session.add(book)
		db.session.commit()	
		return jsonify({"data": "Saved"})

@app.route('/library')
@login_required
def Library():
	image_file = url_for('static', filename='images/' + current_user.image)

	query =  """ select book_id, title, authors, averageRating, thumbnail, pageCount, page, 
	last_read, booked_date from reading join user on user.id = reading.user_id 
	join book on reading.book_id = book.id where user.id = {} """.format(current_user.id)
	q = text(query)
	readings = db.engine.execute(q)
	return render_template('library.html', image=image_file, readings=readings,
		favorites=current_user.favorites, readend=current_user.readends)


@app.route('/readend', methods=['POST'])
@login_required
def ReadEnd():
	res = request.form
	book_id = res['book_id']
	book = Book.query.filter_by(id=book_id).first()
	if book:
		flag = 0
		for bk in current_user.readends:
			if bk.id == book.id:
				flag = 1
				break
		if flag == 1:
			return jsonify({"data": "Already added to read!"})
		current_user.readends.append(book)
		db.session.commit()
		return jsonify({"data": "Successful added to read!"})
	else:
		return jsonify({"data": "failure"})

@app.route('/addfav', methods=['POST'])
@login_required
def AddFav():
	res = request.form
	book_id = res['book_id']
	book = Book.query.filter_by(id=book_id).first()
	if book:
		flag = 0
		for bk in current_user.favorites:
			if bk.id == book.id:
				flag = 1
				break
		if flag == 1:
			return jsonify({"data": "Already added to favorite!"})
		current_user.favorites.append(book)
		db.session.commit()
		return jsonify({"data": "Successful added to favorite!"})
	else:
		return jsonify({"data": "failure"})

@app.route('/removebmk', methods=['POST'])
@login_required
def RemoveBMK():
	res = request.form
	book_id = res['book_id']
	book = Book.query.filter_by(id=book_id).first()
	if book:
		flag = 0
		for bk in current_user.readings:
			if bk.id == book.id:
				flag = 1
				break
		if flag == 1:
			current_user.readings.remove(book)
			db.session.commit()
			return jsonify({"data": "Successful removed from bookmark!"})
		return jsonify({"data": "Already removed from bookmark!"})
	else:
		return jsonify({"data": "failure"})


@app.route('/removefav', methods=['POST'])
@login_required
def RemoveFAV():
	res = request.form
	book_id = res['book_id']
	book = Book.query.filter_by(id=book_id).first()
	if book:
		flag = 0
		for bk in current_user.favorites:
			if bk.id == book.id:
				flag = 1
				break
		if flag == 1:
			current_user.favorites.remove(book)
			db.session.commit()
			return jsonify({"data": "Successful removed from favorite!"})
		return jsonify({"data": "Already removed from favorite!"})
	else:
		return jsonify({"data": "failure"})

@app.route('/removeend', methods=['POST'])
@login_required
def RemoveEND():
	res = request.form
	book_id = res['book_id']
	book = Book.query.filter_by(id=book_id).first()
	if book:
		flag = 0
		for bk in current_user.readends:
			if bk.id == book.id:
				flag = 1
				break
		if flag == 1:
			current_user.readends.remove(book)
			db.session.commit()
			return jsonify({"data": "Successful removed from read!"})
		return jsonify({"data": "Already removed from read!"})
	else:
		return jsonify({"data": "failure"})


@app.route('/track_reading', methods=['POST'])
@login_required
def Track_reading():
	res = request.form
	book_id = res['book_id']
	page = res['page']
	if book_id and page and book_id != "":
		query = 'update reading set page = {} where user_id = {} and book_id = "{}"'.format(page, current_user.id, book_id)
		q = text(query)
		db.engine.execute(q)
		return jsonify({"data": "Successful updated"})
	else:
		return jsonify({"data": "failure"})
		
@app.route('/post', methods=['GET', 'POST'])
@login_required
def Posts():
	image_file = url_for('static', filename='images/' + current_user.image)
	count = 0
	for i in current_user.follow_posts():
		count += 1
	if count < 1:
		posts = Post.query.all()
	else:
		posts = current_user.follow_posts()
	form = MakePost()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data,
			user_id=current_user.id, date_posted=datetime.utcnow())
		db.session.add(post)
		db.session.commit()
		return render_template('post.html', title="Post", image=image_file, form=form, post=posts, time=datetime.utcnow())	
	return render_template('post.html', title="Post", form=form, image=image_file, posts=posts, time=datetime.utcnow())


@app.route('/user/<int:user_id>')
@login_required
def Users(user_id):
	user = User.query.get_or_404(user_id)
	image_file = url_for('static', filename='images/' + current_user.image)
	following, followers, flag = 0, 0, 0
	for u in user.followed:
		following+=1
	for u in user.followers:
		if u.id == current_user.id:
			flag = 1
		followers+=1
	return render_template('user.html', title="User", image=image_file, 
		following=following, user=user, followers=followers, flag=flag)


@app.route('/follow', methods=['POST'])
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


@app.route('/unfollow', methods=['POST'])
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

@app.route('/x')
@login_required
def xxxx():
	x = 0
	print(type(x))
	for i in x:
		print(i)
	return "Hello"








