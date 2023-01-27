# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Test'
app.config['MYSQL_DB'] = 'cloudquicklabs'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		username = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM hospitalaccounts WHERE email = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['hospitalid']
			session['username'] = account['email']
			return render_template('index.html', msg = account)
		else:
			msg = 'Incorrect username or password'
			return render_template('masterloginfail.html', msg = msg)
	return render_template('masterlogin.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'hospitalname' in request.form and 'password' in request.form and 'ownername' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'country' in request.form and 'postalcode' in request.form and 'phonenumber' in request.form and 'dateofsubscription' in request.form and 'pan' in request.form and 'adhaarcard' in request.form and 'gstin' in request.form:
		email = request.form['email']
		hospitalname = request.form['hospitalname']
		password = request.form['password']
		ownername = request.form['ownername']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		phonenumber = request.form['phonenumber']
		dateofsubscription = request.form['dateofsubscription']
		pan = request.form['pan']
		adhaarcard = request.form['adhaarcard']
		gstin = request.form['gstin']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM hospitalaccounts WHERE email = % s', (email, ))
		hospitalaccount = cursor.fetchone()
		if hospitalaccount:
			msg = 'Subscription already exists for email: '+email
			return render_template('registersuccess.html', msg = msg)
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
			return render_template('registerfailure.html', msg = msg)
		elif not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', password):
			msg = 'Valid password has minimum 8 character with atleast one lower case ,one upper case , one digit and one special case..!!'
			return render_template('registerfailure.html', msg = msg)
		else:
			cursor.execute('INSERT INTO hospitalaccounts VALUES (NULL, % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s,  % s)',(password, email, hospitalname, address, city, state, country, postalcode, ownername, phonenumber, dateofsubscription, pan, adhaarcard, gstin))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			return render_template('registersuccess.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM hospitalaccounts WHERE hospitalid = % s', (session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/adminindex")
def adminindex():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM hospitalaccounts WHERE hospitalid = % s', (session['id'], ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['hospitalid']
			session['username'] = account['email']
			return render_template('index.html', msg = account)
	return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			postalcode = request.form['postalcode']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg = msg)
	return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(host ="localhost", port = int("5000"))
