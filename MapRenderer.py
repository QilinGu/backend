# poi.attraction selects tourist attractions.  0x186842
# poi.business selects businesses.   0xff0000
# poi.government selects government buildings. 0x00ff00
# poi.medical selects emergency services, including hospitals, pharmacies, police, doctors, and others. 0x0000ff
# poi.park selects parks. 0x000000
# poi.place_of_worship selects places of worship, including churches, temples, mosques, and others. 0x631355
# poi.school selects schools. 0x584788
# poi.sports_complex selects sports complexes.0x797923
import urllib
from PIL import Image
import requests
from StringIO import StringIO
import time
from flask import Flask, request, jsonify
app = Flask(__name__)
import json


#Get API key from config.txt file
key = open('config.txt').read()
@app.route("/")
def hello():
    return "Hello World!"

#function to get static map image based off of location. Returns image name.
@app.route('/maprender', methods=['POST'])
def map_render(optional_loc=""):
    if optional_loc=="":
        location = json.loads(request.data)
    else:
        location = optional_loc
    #Get latitude, longitude from location dict
    lat  = location['latitude']
    lon = location['longitude']

    #Get and style static google map from api
    URL = "https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=16&size=640x640&maptype=terrain&style=feature:landscape.man_made|color:0x222211&style=feature:all|element:labels|visibility:off&style=feature:road|color:0x654321&style=feature:poi.business|color:0x186842&style=feature:poi.attraction|color:0xff0000&style=feature:poi.government|color:0x00ff00&style=feature:poi.medical|color:0x0000ff&style=feature:poi.park|color:0x000000&style=feature:poi.place_of_worship|color:0x631355&style=feature:poi.school|color:0x584788&style=feature:poi.sports_complex|color:0x797923&key=%s" % (lat, lon, key)
    #Save as image file
    response = requests.get(URL)
    img = Image.open(StringIO(response.content))
    img = img.crop((0,0,640,615))
    t = time.time()
    time_string = "%f" % t
    mult = len(time_string.split('.')[1])
    map_name = "./maps/map_%d.png" % (t * 10**mult)
    img.save(map_name)
    return jsonify({"image_url": map_name})

#Function to return nearby maps based off of last map's center
@app.route('/updatemap', methods=['POST'])
def update_map():
    obj = json.loads(request.data)
    x = obj['x']
    y = obj['y']
    prev = obj['center']
    add_lat = calc_distance_degrees(615,16) * y
    add_lon = calc_distance_degrees(640,16) * x

    #Only return one map if top, left, bottom, or right
    res_map =  json.loads(map_render({'latitude': (prev['latitude'] + add_lat),'longitude': (prev['longitude'] + add_lon)}).data)
    return app.response_class(json.dumps((res_map)), content_type='application/json')

#given number of pixels and zoom level, calculate the distance in latitudinal or longitudinal degrees
def calc_distance_degrees(distance,zoom):
    return (1.0*distance/256)*(360.0 / 2**zoom)


loc = {'latitude': 25.7721638,'longitude': -80.2182310}
#map_render(loc)
#map_render2({'latitude': (25.7721638),'longitude': (-80.2182310 - calc_distance_degrees(640,16))}, 0)
#print update_map("top-left", loc)
if __name__ == "__main__":
    app.run()
