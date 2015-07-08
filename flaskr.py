#-*-coding:utf-8-*-
# all the import
# from __future__ import with_statement
#import sqlite3
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker, scoped_session
from db_setup import Base, Entries, Board1, Board2
# import MySQLdb as mariadb
from flask import Flask, request, g, redirect, url_for, abort, render_template, flash
from flask import session as login_session
# from contextlib import closing
import sys

#configuration
# DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = '1234'
USERNAME = 'admin'
PASSWORD = 'wjdtnsgud1!'

#create our little application
app=Flask(__name__)
app.config.from_object(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

#Connect to Database and create database session
engine = create_engine("mysql://root:wjdtnsgud1!@localhost/annonymous", encoding='utf8', echo=False)
Base.metadata.bind = engine

# DBSession = sessionmaker()
DBSession=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# DBSession.configure(bind=engine)
session = DBSession()

# def connect_db():
# 	return mariadb.connect('localhost','root', 'wjdtnsgud1!','annonymous')
#	return sqlite3.connect(app.config['DATABASE'])

# def init_db():
# 	with closing(connect_db()) as db:
# 		with app.open_resource('schema.sql') as f:
# 			db.cursor().executescript(f.read())
# 		db.commit()

# @app.before_request
# def before_request():
# 	con=connect_db()
# #	g.db=connect_db()
	
# @app.teardown_request
# def teardown_request(exception):
# #	g.db.close()
# 	con.close()

# @app.route('/')
# def show_entries():
# 	con=connect_db()
# 	cursor=con.cursor()
# 	cursor.execute('select title, text from entries order by id desc')
# 	entries=[dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
# 	cursor.close()
# 	con.close()
# 	return render_template('show_entries.html', entries=entries)

@app.route('/')
def show_entries():
	entries=session.query(Entries).order_by(desc(Entries.id)).all()
	session.close()
	return render_template('show_entries.html',entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
	# con=connect_db()
	# cursor=con.cursor()
	# cursor.execute('insert into entries (title, text) values (%s,%s)',[request.form['title'].encode('utf-8'), request.form['text'].encode('utf-8')])
	# con.commit()
	# cursor.close()
	# con.close()
	newEntry=Entries(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
	session.add(newEntry)
	session.commit()
	flash('글이 게시되었어!')
	session.close()
	return redirect(url_for('show_entries'))

@app.route('/add1', methods=['POST'])
def add1():
	newBoard1=Board1(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
	session.add(newBoard1)
	session.commit()
	flash('글이 게시되었어!')
	session.close()
	return redirect(url_for('board1'))

@app.route('/add2', methods=['POST'])
def add2():
	newBoard2=Board2(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
	session.add(newBoard2)
	session.commit()
	flash('글이 게시되었어!')
	session.close()
	return redirect(url_for('board2'))

@app.route('/login', methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username'] != app.config['USERNAME']:
			error='invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error='invalid password'
		else:
			login_session['logged_in']=True
			flash('로그인 되었습니다.')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	login_session.pop('logged_in', None)
	flash('로그아웃되었습니다.')
	return redirect(url_for('show_entries'))

@app.route('/board1')
def board1():
	writings1=session.query(Board1).order_by(desc(Board1.id)).all()
	session.close()
	return render_template('board1.html', writings1=writings1)

@app.route('/board2')
def board2():
	writings2=session.query(Board2).order_by(desc(Board2.id)).all()
	session.close()
	return render_template('board2.html', writings2=writings2)

@app.teardown_request
def shutdown_session(exception=None):
	DBSession.remove()

if __name__=='__main__':
	app.run(host='0.0.0.0')