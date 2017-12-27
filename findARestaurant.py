from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "P0R4TNSJ34MYDW5DITIXQ5SB5YAWTFJKEIKHI3EHZNS10MKB"
foursquare_client_secret = "OUZOBXI133ETHMNVCHVTYXME4AKHPZMHTU4IQNHM3K4LC0WX"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	#print "="*len(location)
	#print location
	#print "="*len(location)
	#print latitude
	#print longitude
	
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s&limit=1' %(foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))

	h = httplib2.Http()
	response, content = h.request(url,'GET')
	result = json.loads(content)
	print "=" * 100
	print result
	print "=" * 100
	#3. Grab the first restaurant
	first_restaurant = result["response"]["venues"][0]["name"]
	print first_restaurant
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	img_url = result["response"]["venues"][0]["categories"][0]["icon"]["prefix"]
	file_type = result["response"]["venues"][0]["categories"][0]["icon"]["suffix"]
	
	img_url += file_type
	print img_url
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url	
if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
