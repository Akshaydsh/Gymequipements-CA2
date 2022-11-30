from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from passlib.hash import sha256_crypt
from flask_script import Manager
from functools import wraps
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'eswar@259522'
app.config['MYSQL_DB'] = 'Gym'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Nice try, Tricks don\'t work, bud!! Please Login :)', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_trainor(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 3:
			return f(*args, **kwargs)
		else:
			flash('You are probably not a trainor!!, Are you?', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 1:
			return f(*args, **kwargs)
		else:
			flash('You are probably not an admin!!, Are you?', 'danger')
			return redirect(url_for('login'))
	return wrap

if __name__ == "__main__":
	app.secret_key = '528491@JOKER'
	app.debug = True
	manager = Manager(app)
	#manager.secret_key = '528491@siva'
	manager.run()
	#app.run()



