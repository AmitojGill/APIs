from flask import Flask, render_template, g, jsonify
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///paleKale.db')
DBsession = sessionmaker(bind=engine)
session = DBsession()



app = Flask(__name__)

@app.route('/clientOAuth')
def start():
	return render_template('clientOAuth.html')

@auth.verify_password
def verify_password(username_or_token, password):
	user_id = User.verify_auth_token(username_or_token)
	if user_id:
		user = session.query(User).filter_by(id = user_id).one()
	else:
		user = session.query(User).filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

@app.route('/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})

@app.route('/users', methods =['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	#Check to see if username of password are blank
	if username is None or password is None:
		print "missing arguments"
		abort(400)

	#check to see if user already exist in the db
	if session.query(User).filter_by(username = username).first() is not None:
		print "existing user"
		user = session.query(User).filter_by(username=username).first()
		return jsonify({'message':'user already exists'}), 200

	#Create a New user
	user = User(username = username)
	user.hash_password(password)
	session.add(user)
	session.commit()
	return jsonfiy({'username': user.username}), 201



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=5000)