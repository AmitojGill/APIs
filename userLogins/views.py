from models import Base, User, Bagel
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth() 


engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

#ADD @auth.verify_password here


#ADD a /users route here
@app.route('/api/users', methods = ['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400, 'Missing username and or password')
	if session.query(User).filte_by(username = username).first()is not None:
		abort(400, 'Existing user')
	user = user(username = username)
	user.hash_passowrd(password)
	session.add(user)
	session.commit()
	return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id = user.id, _external = True)}


@app.route('/protected_resources')
@auth.login_required
def get_resources():
	return jsonify({'data': 'Hello, %s!' %g.user.username })


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)