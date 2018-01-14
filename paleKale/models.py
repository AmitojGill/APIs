from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(32), index=True)
	picture = Column(String)
	email = Column(String)
	password_hash = Column(String(64))

engine = create_engine('sqlite:///usersWithOAuth.db')

Base.metadata.create_all(engine)