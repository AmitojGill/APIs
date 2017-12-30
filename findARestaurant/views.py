from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
  if request.method == 'GET':
  	restaurants = session.query(Restaurant).all()
  	return jsonify(restaurants = [i.serialize for i in restaurants])
  elif request.method == 'POST':
  	location = request.args.get('location','')
  	mealType = request.args.get('mealType','')
  	restaurantInfo = findARestaurant(mealType, location)
  	if restaurantInfo != "No Restaurants Found":
  		newRestaurant = Restaurant(restaurant_name = unicode(restaurantInfo['name']),
  		restaurant_address = unicode(restaurantInfo['address']),
  		restaurant_image = restaurantInfo['image'])
  		session.add(newRestaurant)
  		session.commit()
  		return jsonify(restaurant = newRestaurant.serialize)
  	else:
  		return jsonify({'error': 'No Restaurants found for %s in %s' % (mealType,location)})


    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  restaurant = session.query(Restaurant).filter_by(id=id).one()
  if request.method == 'GET':
  	return jsonify(restaurant = restaurant.serialize)
  elif request.method == "PUT":
  	name = request.args.get('name')
  	address = request.args.get('location')
  	image = request.args.get('image')
  	if name:
  		restaurant.name = name
  	if image:
  		restaurant.image = image
  	if address:
  		restaurant.address = address
  	session.commit()
  	return jsonify(restaurant = restaurant.serialize)
  elif request.method == "DELETE":
  	session.delete(restaurant)
  	session.commit()
  	return "Restaurant Deleted"


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)