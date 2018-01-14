from flask import Flask
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///usersWithOauth.db')
DBsession = sessionmaker(bind=engine)
session = DBsession()



app = Flask(__name__)



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=5000)