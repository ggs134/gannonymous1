from flask import Flask, url_for
app=Flask(__name__)

@app.route('/')
def index():
	return 'hello, world!'

@app.route('/user/<username>')
def show_user_profile(username):
	return 'User %s' %username

@app.route('/user/<int:post_id>')
def show_post(post_id):
	return 'Post %d' %post_id

@app.route('/login')
def login():pass

with app.test_request_context():
	print url_for('index')
	print url_for('login')
	print url_for('login',next='/')
	print url_for('show_user_profile',username='Kevin')

if __name__=='__main__':
	app.run(debug=True)
