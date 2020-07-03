#!/usr/local/python/3.4/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import flash, redirect, url_for, session, request, logging
from flask import render_template as template
from wtforms import Form, SelectField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from data import Index_display101, Index_display102
import os
from datetime import datetime

#データベースの絶対パス
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(basedir, 'db', 'linuc.sqlite3')

#Flaskアプリケーションクラスのインスタンスを新規生成
app = Flask(__name__)

#アプリケーションの設定を追加
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['secret_key'] = 'YQZXzmAJXwD24dimt1QluyqtZO'

#Flaskアプリケーションを新規で生成する関数を定義
def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = db_path
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = False
	db.init_app(app)
	app.config['secret_key'] = 'YQZXzmAJXwD24dimt1QluyqtZO'
	return app


#configurationクラスを別のモジュールで作っているときはこうやって一括で設定する
# app.config.from_object('config.Config')


#SQLSlchemyクラスのインスタンスを新規生成
db = SQLAlchemy(app)


#テーブルに相当するクラスを設定
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), unique=True, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

	def __repr__(self):
		return '<Users %r>' % self.username

class Articles(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(29), unique=True, nullable=False)
	chapter = db.Column(db.String(9), unique=False, nullable=False)
	title = db.Column(db.String(99), unique=False, nullable=False)
	body = db.Column(db.Text, unique=False, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

	def __repr__(self):
		return '<Articles %r>' % self.title

class Practices(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	chapter = db.Column(db.String(9), unique=False, nullable=False)
	question = db.Column(db.Text, unique=False, nullable=False)
	choice1 = db.Column(db.String(49), unique=False, nullable=False)
	choice2 = db.Column(db.String(49), unique=False, nullable=False)
	choice3 = db.Column(db.String(49), unique=False, nullable=False)
	choice4 = db.Column(db.String(49), unique=False, nullable=False)	#選択肢は３から４個
	answer = db.Column(db.String(49), unique=False, nullable=False)
	explanation = db.Column(db.Text, unique=False, nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

	def __repr__(self):
		return '<Practices %r>' % self.question

# Register Form Class
class RegisterForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=25)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# Article Form Class
class ArticleForm(Form):
	chapter = SelectField('Chapter', choices=[('1', '1章'), ('2', '2章'), ('3', '3章'), ('4', '4章'), ('5', '5章'), ('6', '6章'), ('7', '7章'), ('8', '8章'), ('9', '9章'), ('10', '10章')])
	url = StringField('Url', [validators.Length(min=1, max=200)])
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=10)])

# Practice Form Class
class PracticeForm(Form):
	# クラス変数を定義
	chapter = SelectField('Chapter', choices=[('1', '1章'), ('2', '2章'), ('3', '3章'), ('4', '4章'), ('5', '5章'), ('6', '6章'), ('7', '7章'), ('8', '8章'), ('9', '9章'), ('10', '10章')])
	question = TextAreaField('問題', [validators.Length(min=10)])
	choice1 = StringField('選択肢1', [validators.Length(min=1, max=100)])
	choice2 = StringField('選択肢2', [validators.Length(min=1, max=100)])
	choice3 = StringField('選択肢3', [validators.Length(min=1, max=100)])
	choice4 = StringField('選択肢4', [validators.Length(min=1, max=100)])
	answer = StringField('答え', [validators.Length(min=1, max=100)])
	explanation = TextAreaField('解説', [validators.Length(min=10)])

#home data
index_chapter_list101 = Index_display101()
index_chapter_list102 = Index_display102()


#routing

@app.route('/')
@app.route('/home')
def index():
	return template("index.html", list101 = index_chapter_list101, list102 = index_chapter_list102,)


@app.route('/about')
def about():
	return template("about.html")

@app.route('/xtermjs')
def xtermjs():
	return template("xtermjs.html")

@app.route('/practice/<string:practice_id>', methods = ['GET', 'POST'])
def practice(practice_id):
	# connection = engine.connect()


	result = Practices.query.filter_by(id=practice_id).first()
	# stmt = select([practices]).where(practices.columns.id == practice_id)
	# result_proxy = connection.execute(stmt)
	# result = result_proxy.fetchone()

	# connection.close()

	if request.method == 'POST':
 	#get form fields
		choice = request.form['choice']

		return template("practice.html", practice=result, choice=choice)

	return template("practice.html", practice=result)

# by chapter
@app.route('/chapter/<string:chapter_id>')
def chapter(chapter_id):
    #connect the database
	# connection = engine.connect()

	#fetch the row
	results = Articles.query.filter_by(chapter=chapter_id).all()
	# stmt = select([articles]).where(articles.columns.chapter == chapter_id)
	# result_proxy = connection.execute(stmt)
	# results = result_proxy.fetchall()

	# Close connection
	# connection.close()

	if results:
		return template('chapter.html', articles=results)
	else:
		msg = 'No Articles Found'
		return template('chapter.html', msg=msg)

    
#Display Single Article
@app.route('/article/<string:article_url>')
def article(article_url):

	#fetch the row
	result = Articles.query.filter_by(url=article_url).first()
	# stmt = select([articles]).where(articles.columns.id == article_id)
	# result_proxy = connection.execute(stmt)
	# result = result_proxy.fetchone()

	# connection.close()

	if result:
		return template('article.html', article=result)
	else:
		msg = 'No Articles Found'
		return template('article.html', msg=msg)


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# Create cursor
		result = Users(username=username, password=password)
		db.session.add(result)
		db.session.commit()

		flash('You are now registered and can log in', 'success')

		return redirect(url_for('login'))
	return template('register.html', form=form)

#login
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		#get form fields
		username = request.form['username']
		password_candidate = request.form['password']

		#connect the database
		# connection = engine.connect()

		#fetch the row
		result = Users.query.filter_by(username=username).first()
		# stmt = select([users]).where(users.columns.username == username)
		# result = connection.execute(stmt).fetchone()

		# connection.close()

		if result:
			if sha256_crypt.verify(password_candidate, result.password):
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))

			else:
				error = 'Invalid Login'
				return template('login.html', error=error)

		else:
			error = 'Username Not Found'
			return template('login.html', error=error)

	return template("login.html")


def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
 			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap


@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():

	# Connect the database
	# connection = engine.connect()

	# Get articles
	article_results = Articles.query.all()
	# stmt = select([articles])
	# result_proxy = connection.execute(stmt)
	# article_results = result_proxy.fetchall()

	practice_results = Practices.query.all()
	# stmt = select([practices])
	# result_proxy = connection.execute(stmt)
	# practice_results = result_proxy.fetchall()

	# Close connection
	# connection.close()
	
	if article_results and practice_results:
		return template('dashboard.html', articles=article_results, practices=practice_results)
	elif article_results and not practice_results:
		msg = 'No Practices Found'
		return template('dashboard.html', articles=article_results, msg=msg)
	elif not article_results and practice_results:
		msg = 'No Articles Found'
		return template('dashboard.html', practices=practice_results, msg=msg)
	else:
		msg = 'No Articles And Practices Found'
		return template('dashboard.html', msg=msg)


# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		url = form.url.data
		chapter = form.chapter.data
		title = form.title.data
		body = form.body.data

		#insert the data
		result = Articles(url=url, chapter=chapter, title=title, body=body)
		db.session.add(result)
		db.session.commit()
		# stmt = insert(articles).values(chapter=chapter, title=title, body=body)
		# result_proxy = connection.execute(stmt)

        # Commit to DB
        # mysql.connection.commit()

        #Close connection
		# connection.close()

		flash('Article Created', 'success')

		return redirect(url_for('dashboard'))

	return template('add_article.html', form=form)


# Add Practice
@app.route('/add_practice', methods=['GET', 'POST'])
@is_logged_in
def add_practice():
	# インスタンスを生成
	form = PracticeForm(request.form)
	if request.method == 'POST' and form.validate():
		chapter = form.chapter.data
		question = form.question.data
		choice1 = form.choice1.data
		choice2 = form.choice2.data
		choice3 = form.choice3.data
		choice4 = form.choice4.data
		answer = form.answer.data
		explanation = form.explanation.data

        #connect the database
		# connection = engine.connect()

		#insert the data
		result = Practices(chapter=chapter, question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, answer=answer, explanation=explanation)
		db.session.add(result)
		db.session.commit()
		# stmt = insert(practices).values(chapter=chapter, question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, answer=answer, explanation=explanation)
		# result_proxy = connection.execute(stmt)

        #Close connection
		# connection.close()

		flash('Practice Created', 'success')

		return redirect(url_for('dashboard'))

	return template('add_practice.html', form=form)



# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	# Get article by id
	result = Articles.query.filter_by(id=id).first()
    
	# Get form
	form = ArticleForm(request.form)

	# Populate article form fields
	form.url.data = result.url
	form.chapter.data = result.chapter
	form.title.data = result.title
	form.body.data = result.body

	if request.method == 'POST' and form.validate():
		url = request.form['url']
		chapter = request.form['chapter']
		title = request.form['title']
		body = request.form['body']

        # Create Cursor
		# connection = engine.connect()

        # Execute
		result = Articles.query.filter_by(id=id).first()
		result.url = url
		result.chapter = chapter
		result.title = title
		result.body = body
		db.session.add(result)
		db.session.commit()

		#Close connection
		# connection.close()

		flash('Article Updated', 'success')

		return redirect(url_for('dashboard'))

	return template('edit_article.html', form=form)


# Edit Practice
@app.route('/edit_practice/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_practice(id):
	# Get article by id
	result = Practices.query.filter_by(id=id).first()
    
	# Get form
	form = PracticeForm(request.form)

	# Populate article form fields
	form.chapter.data = result.chapter
	form.question.data = result.question
	form.choice1.data = result.choice1
	form.choice2.data = result.choice2
	form.choice3.data = result.choice3
	form.choice4.data = result.choice4
	form.answer.data = result.answer
	form.explanation.data = result.explanation

	if request.method == 'POST' and form.validate():
		chapter = request.form['chapter']
		question = request.form['question']
		choice1 = request.form['choice1']
		choice2 = request.form['choice2']
		choice3 = request.form['choice3']
		choice4 = request.form['choice4']
		answer = request.form['answer']
		explanation = request.form['explanation']

		# Execute
		practice = Practices.query.filter_by(id=id).first()
		practice.chapter = chapter
		practice.question = question
		practice.choice1 = choice1
		practice.choice2 = choice2
		practice.choice3 = choice3
		practice.choice4 = choice4
		practice.answer = answer
		practice.explanation = explanation

		db.session.add(practice)
		db.session.commit()

		flash('Practice Updated', 'success')

		return redirect(url_for('dashboard'))

	return template('edit_practice.html', form=form)


# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):

	result = Articles.query.filter_by(id=id).first()

	db.session.delete(result)
	db.session.commit()

	flash('Article Deleted', 'success')

	return redirect(url_for('dashboard'))


# Delete Practice
@app.route('/delete_practice/<string:id>', methods=['POST'])
@is_logged_in
def delete_practice(id):

	result = Practices.query.filter_by(id=id).first()

	db.session.delete(result)
	db.session.commit()

	flash('Practice Deleted', 'success')

	return redirect(url_for('dashboard'))


#サーバーの起動
if __name__ == '__main__':
	app.run(debug=True)