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
	
	if result["response"]["venues"]:
		#3. Grab the first restaurant
		restaurant = result["response"]["venues"][0]
		venue_id = restaurant["id"]
		restaurant_name = restaurant["name"]
		restaurant_address = restaurant['location']["formattedAddress"]
		address = ""
		for i in restaurant_address:
			address += i + " "
		restaurant_address = address

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' %(venue_id, foursquare_client_id, foursquare_client_secret))
		h = httplib2.Http()
		response, content = h.request(url, 'GET')
		result = json.loads(content)

		count = result['response']['photos']['count']
	#5. Grab the first image
		if result['response']['photos']['items']:
			firstPic = result['response']['photos']['items'][0]
			prefix = firstPic['prefix']
			suffix = firstPic['suffix']
			img_size = "300x300"
			img_url = prefix + img_size + suffix
		else:
	#6. If no image is available, insert default a image url
			img_url = "https://cdn.pixabay.com/photo/2017/12/28/12/32/set-3045129_1280.jpg"
	#7. Return a dictionary containing the restaurant name, address, and image url
		restaurantInfo = {'name': restaurant_name, 'address': restaurant_address, 'image': img_url}
		print "Restaurant Name: %s" % restaurantInfo['name']
		print "Restaurant Address: %s" % restaurantInfo['address']
		print "Image: %s \n" % restaurantInfo['image']
		return restaurantInfo
	else:
		print "No restaurant found for %s" % location
		return "No Restaurants Found"

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
