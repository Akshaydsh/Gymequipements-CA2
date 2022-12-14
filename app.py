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

def is_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 1:
			return f(*args, **kwargs)
		else:
			flash('You are probably not an admin!!, Are you?', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_recep_level(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] <= 2:
			return f(*args, **kwargs)
		else:
			flash('You are probably not an authorised to view that page!!', 'danger')
			return redirect(url_for('login'))
	return wrap


@app.route('/')
def index():
	return render_template('home.html')	

	@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']

		cur = mysql.connection.cursor()

		result = cur.execute('SELECT * FROM info WHERE username = %s', [username])
		#print(result)
		if result>0:
			data = cur.fetchone()
			password = data['password']

			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['username'] = username
				session['prof'] = data['prof']
				#session['hash'] = sha256_crypt.encrypt(username)
				flash('You are logged in', 'success')
				if session['prof'] == 1:
					return redirect(url_for('adminDash'))
				if session['prof'] == 3:
					return redirect(url_for('trainorDash'))
				if session['prof'] == 2:
					return redirect(url_for('recepDash'))
				#s = 'memberDash/%s', (username)
				return redirect(url_for('memberDash', username = username))
			else:
				error = 'Invalid login'
				return render_template('login.html', error = error)

			cur.close();
		else:
			error = 'Username NOT FOUND'
			return render_template('login.html', error = error)

	return render_template('login.html')


class ChangePasswordForm(Form):
	old_password = PasswordField('Existing Password')
	new_password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords aren\'t matching pal!, check \'em')
	])
	confirm = PasswordField('Confirm Password')


@app.route('/update_password/<string:username>', methods = ['GET', 'POST'])
def update_password(username):
	form = ChangePasswordForm(request.form)
	if request.method == 'POST' and form.validate():
		new = form.new_password.data
		entered = form.old_password.data
		cur = mysql.connection.cursor()
		cur.execute("SELECT password FROM info WHERE username = %s", [username])
		old = (cur.fetchone())['password']
		if sha256_crypt.verify(entered, old):
			cur.execute("UPDATE info SET password = %s WHERE username = %s", (sha256_crypt.encrypt(new), username))
			mysql.connection.commit()
			cur.close()
			flash('New password will be in effect from next login!!', 'info')
			return redirect(url_for('memberDash', username = session['username']))
		cur.close()
		flash('Old password you entered is wrong!!, try again', 'warning')
	return render_template('updatePassword.html', form = form)

class DeleteRecepForm(Form):
	username = SelectField(u'Choose which one you wanted to delete', choices=choices)



@app.route('/deleteTrainor', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def deleteTrainor():
	choices.clear()
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT username FROM trainors")
	b = cur.fetchall()
	for i in range(q):
		tup = (b[i]['username'],b[i]['username'])
		choices.append(tup)
	form = DeleteRecepForm(request.form)
	if len(choices)==1:
		flash('You cannot remove your only Trainor!!', 'danger')
		return redirect(url_for('adminDash'))
	if request.method == 'POST':
		#app.logger.info(form.username.data)
		username = form.username.data
		q = cur.execute("SELECT username FROM trainors WHERE username != %s", [username])
		b = cur.fetchall()
		new = b[0]['username']
		cur.execute("UPDATE members SET trainor = %s WHERE trainor = %s", (new, username))
		cur.execute("DELETE FROM trainors WHERE username = %s", [username])
		cur.execute("DELETE FROM info WHERE username = %s", [username])
		mysql.connection.commit()
		cur.close()
		choices.clear()
		flash('You removed your Trainor!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('deleteRecep.html', form = form)


@app.route('/addRecep', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addRecep():
	values.clear()
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT username FROM info")
	b = cur.fetchall()
	for i in range(q):
		values.append(b[i]['username'])
	#app.logger.info(b[0]['username'])
	#res = values.fetchall()
	#app.logger.info(res)
	cur.close()
	form = AddTrainorForm(request.form)
	if request.method == 'POST' and form.validate():
		#app.logger.info("setzdgxfhcgjvkhbjlkn")
		name = form.name.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		street = form.street.data
		city = form.city.data
		phone = form.phone.data

		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO info(name, username, password, street, city, prof, phone) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, username, password, street, city, 2,phone))
		cur.execute("INSERT INTO receps(username) VALUES(%s)", [username])
		mysql.connection.commit()
		cur.close()
		flash('You recruited a new Receptionist!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('addRecep.html', form=form)


class DeleteRecepForm(Form):
	username = SelectField(u'Choose which one you wanted to delete', choices=choices)



@app.route('/deleteRecep', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def deleteRecep():
	choices.clear()
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT username FROM receps")
	b = cur.fetchall()
	for i in range(q):
		tup = (b[i]['username'],b[i]['username'])
		choices.append(tup)
	if len(choices)==1:
		flash('You cannot remove your only receptionist!!', 'danger')
		return redirect(url_for('adminDash'))
	form = DeleteRecepForm(request.form)
	if request.method == 'POST':
		#app.logger.info(form.username.data)
		username = form.username.data
		cur.execute("DELETE FROM receps WHERE username = %s", [username])
		cur.execute("DELETE FROM info WHERE username = %s", [username])
		mysql.connection.commit()
		cur.close()
		choices.clear()
		flash('You removed your receptionist!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('deleteRecep.html', form = form)


class AddEquipForm(Form):
	name = StringField('Name', [validators.Length(min = 1, max = 100)])
	count = IntegerField('Count', [validators.NumberRange(min = 1, max = 25)])


@app.route('/addEquip', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addEquip():
	form = AddEquipForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		count = form.count.data
		cur = mysql.connection.cursor()
		q = cur.execute("SELECT name FROM equip")
		equips = []
		b = cur.fetchall()
		for i in range(q):
			equips.append(b[i]['name'])
		if name in equips:
			cur.execute("UPDATE equip SET count = count+%s WHERE name = %s", (count, name))
		else:
			cur.execute("INSERT INTO equip(name, count) VALUES(%s, %s)", (name, count))
		mysql.connection.commit()
		cur.close()
		flash('You added a new Equipment!!', 'success')
		return redirect(url_for('adminDash'))
	return render_template('addEquip.html', form = form)

class RemoveEquipForm(Form):
	name = RadioField('Name', choices = choices)
	count = IntegerField('Count', [validators.InputRequired()])

if __name__ == "__main__":
	app.secret_key = '528491@JOKER'
	app.debug = True
	manager = Manager(app)
	#manager.secret_key = '528491@siva'
	manager.run()
	#app.run()


class AddMemberForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username already taken, Please try another")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    plan  = RadioField('Select Plan', choices = choices)
    trainor = SelectField('Select Trainor', choices = choices2)
    street = StringField('Street', [validators.Length(min = 1, max = 100)])
    city = StringField('City', [validators.Length(min = 1, max = 100)])
    phone = StringField('Phone', [validators.Length(min = 1, max = 100)])
@app.route('/addMember', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def addMember():
	choices.clear()
	choices2.clear()
	cur = mysql.connection.cursor()
	
	q = cur.execute("SELECT username FROM info")
	b = cur.fetchall()
	for i in range(q):
		values.append(b[i]['username'])
	
	q = cur.execute("SELECT DISTINCT name FROM plans")
	b = cur.fetchall()
	for i in range(q):
		tup = (b[i]['name'],b[i]['name'])
		choices.append(tup)
	
	q = cur.execute("SELECT username FROM trainors")
	b = cur.fetchall()
	for i in range(q):
		tup = (b[i]['username'],b[i]['username'])
		choices2.append(tup)
	
	cur.close()
	
	form = AddMemberForm(request.form)
	if request.method == 'POST' and form.validate():
		#app.logger.info("setzdgxfhcgjvkhbjlkn")
		name = form.name.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		street = form.street.data
		city = form.city.data
		phone = form.phone.data
		plan = form.plan.data
		trainor = form.trainor.data
		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO info(name, username, password, street, city, prof, phone) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, username, password, street, city, 4,phone))
		cur.execute("INSERT INTO members(username, plan, trainor) VALUES(%s, %s, %s)", (username, plan, trainor))
		mysql.connection.commit()
		cur.close()
		choices2.clear()
		choices.clear()
		flash('You added a new member!!', 'success')
		if(session['prof']==1):
			return redirect(url_for('adminDash'))
		return redirect(url_for('recepDash'))
	return render_template('addMember.html', form=form)


@app.route('/deleteMember', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def deleteMember():
	choices.clear()
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT username FROM members")
	b = cur.fetchall()
	for i in range(q):
		tup = (b[i]['username'],b[i]['username'])
		choices.append(tup)
	form = DeleteRecepForm(request.form)
	if request.method == 'POST':
		username = form.username.data
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM members WHERE username = %s", [username])
		cur.execute("DELETE FROM info WHERE username = %s", [username])
		mysql.connection.commit()
		cur.close()
		choices.clear()
		flash('You deleted a member from the GYM!!', 'success')
		if(session['prof']==1):
			return redirect(url_for('adminDash'))
		return redirect(url_for('recepDash'))
	return render_template('deleteRecep.html', form = form)

@app.route('/viewDetails')
def viewDetails():
	cur = mysql.connection.cursor()
	cur.execute("SELECT username FROM info WHERE username != %s", [session['username']])
	result = cur.fetchall()
	return render_template('viewDetails.html', result = result)


@app.route('/recepDash')
@is_recep_level
def recepDash():
	return render_template('recepDash.html')