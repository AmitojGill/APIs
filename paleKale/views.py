from flask import Flask, render_template
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


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=5000)