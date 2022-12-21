from datetime import datetime
from ReBook import db
from datetime import datetime
from sqlalchemy import text
from flask import render_template, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from ReBook.models import User, Book, Post
from ReBook.posts.forms import MakePost


posts = Blueprint('posts', __name__)


@posts.route('/post', methods=['GET', 'POST'])
@login_required
def Posts():
	page = request.args.get('page', 1, type=int)
	image_file = url_for('static', filename='images/' + current_user.image)
	count = 0
	for i in current_user.follow_posts().items:
		count += 1
	if count < 1:
		posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=25)
	else:
		posts = current_user.follow_posts()
	form = MakePost()

	following, followers = 0, 0
	for u in current_user.followed:
		following+=1
	for u in current_user.followers:
		followers+=1

	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data,
			user_id=current_user.id, date_posted=datetime.utcnow())
		db.session.add(post)
		db.session.commit()
		form.title.data, form.content.data="", ""
		render_template("blog.html", image=image_file, form=form, 
			posts=posts, time=datetime.utcnow(), followers=followers, following=following, page=page)
	return render_template("blog.html", form=form, image=image_file,
	 posts=posts, time=datetime.utcnow(), followers=followers, following=following, page=page)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('posts.Posts'))


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	image_file = url_for('static', filename='images/' + current_user.image)
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = MakePost()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		return redirect(url_for('posts.Posts'))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template("change.html", form=form, image=image_file, time=datetime.utcnow())


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
	image_file = url_for('static', filename='images/' + current_user.image)
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	return render_template("post.html", post=post, image=image_file)
