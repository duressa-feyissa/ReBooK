from flask import render_template, url_for, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/home')
@main.route('/')
def mainRoute():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('layout.html', image=image_file)
	return render_template('layout.html')
	
@main.route('/advanced')
def advancedRoute():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('advanced.html', image=image_file)
	return render_template('advanced.html')

@main.route('/about')
def About():
	if current_user.is_authenticated:
		image_file = url_for('static', filename='images/' + current_user.image)
		return render_template('about.html', image=image_file)
	return render_template('about.html')


