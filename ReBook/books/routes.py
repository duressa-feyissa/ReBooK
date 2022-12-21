from sqlalchemy import text
from flask import render_template, request, jsonify, url_for, Blueprint
from ReBook.parse import parse
from flask_login import current_user, login_required
from ReBook.models import Book
from ReBook import db

books = Blueprint('books', __name__)

@books.route('/book')
def bookRoute():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('view.html', image=image_file)
	return render_template('view.html')

@books.route('/process', methods=['POST'])
def process():
	res = request.form
	data = parse(res)
	return jsonify(data)

@books.route('/save', methods=["GET", "POST"])
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

@books.route('/library')
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


@books.route('/readend', methods=['POST'])
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


@books.route('/addfav', methods=['POST'])
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

@books.route('/removebmk', methods=['POST'])
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


@books.route('/removefav', methods=['POST'])
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


@books.route('/removeend', methods=['POST'])
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


@books.route('/track_reading', methods=['POST'])
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
