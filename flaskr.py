#-*-coding:utf-8-*-
# all the import
from __future__ import with_statement
#import sqlite3
import MySQLdb as mariadb
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
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

def connect_db():
	return mariadb.connect('localhost','root', 'wjdtnsgud1!','annonymous')
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

@app.route('/')
def show_entries():
#	cur=g.db.execute('select title, text from entries order by id desc')
	con=connect_db()
	cursor=con.cursor()
	cursor.execute('select title, text from entries order by id desc')
	entries=[dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
	cursor.close()
	con.close()
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	# if not session.get('logged_in'):
	# 	abort(401)
	con=connect_db()
	cursor=con.cursor()
	cursor.execute('insert into entries (title, text) values (%s,%s)',[request.form['title'].encode('utf-8'), request.form['text'].encode('utf-8')])
	con.commit()
	cursor.close()
	con.close()
#	con.cursor().execute('insert into entries (title, text) values (?,?)',[request.form['title'], request.form['text']])
#	con.commit()
	flash('글이 게시되었어!')
	return redirect(url_for('show_entries'))

@app.route('/add1', methods=['POST'])
def add1():
	# if not session.get('logged_in'):
	# 	abort(401)
	con=connect_db()
	cursor=con.cursor()
	cursor.execute('insert into board1 (title, text) values (%s,%s)',[request.form['title'].encode('utf-8'), request.form['text'].encode('utf-8')])
	con.commit()
	cursor.close()
	con.close()
#	con.cursor().execute('insert into entries (title, text) values (?,?)',[request.form['title'], request.form['text']])
#	con.commit()
	flash('글이 올라갔어!')
	return redirect(url_for('board1'))

@app.route('/add2', methods=['POST'])
def add2():
	# if not session.get('logged_in'):
	# 	abort(401)
	con=connect_db()
	cursor=con.cursor()
	cursor.execute('insert into board2 (title, text) values (%s,%s)',[request.form['title'].encode('utf-8'), request.form['text'].encode('utf-8')])
	con.commit()
	cursor.close()
	con.close()
#	con.cursor().execute('insert into entries (title, text) values (?,?)',[request.form['title'], request.form['text']])
#	con.commit()
	flash('글이 올라갔어!')
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
			session['logged_in']=True
			flash('로그인 되었습니다.')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('로그아웃되었습니다.')
	return redirect(url_for('show_entries'))

@app.route('/board1')
def board1():
	con=connect_db()
	cursor=con.cursor()
	cursor.execute('select title,text from board1 order by id desc')
	writings1=[dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
	cursor.close()
	con.close()
	return render_template('board1.html', writings1=writings1)

@app.route('/board2')
def board2():
	con=connect_db()
	cursor=con.cursor()
	cursor.execute('select title,text from board2 order by id desc')
	writings2=[dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
	cursor.close()
	con.close()
	return render_template('board2.html', writings2=writings2)

if __name__=='__main__':
	app.run(host='0.0.0.0')
