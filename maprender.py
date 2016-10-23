import urllib
from PIL import Image
import requests
from StringIO import StringIO
import time
import os
from random import random, uniform

#Get API key from .env
key = os.getenv("GOOGLE_API_KEY")
def get_map(location):
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
    return map_name

def get_new_map(x,y,center):
    add_lat = calc_distance_degrees(615,16) * y
    add_lon = calc_distance_degrees(640,16) * x
    return get_map({'latitude': (center['latitude'] + add_lat),'longitude': (center['longitude'] + add_lon)})

def get_objects(num, center):
    obj = []
    for i in range(num):
        if i <5:
            lon = calc_distance_degrees(uniform(15,50), 16)
            lat = calc_distance_degrees(uniform(15,50), 16)
        else:
            lon = calc_distance_degrees(uniform(15,320), 16)
            lat = calc_distance_degrees(uniform(15,307.5), 16)
        if random() > 0.5:
            lon * -1
        if random() > 0.5:
            lat * -1
        enemy_name = "enemy%d" % i
        obj.append({
        "type" : "ai",
        "latitude": center["latitude"] + lat,
        "longitude": center["longitude"] + lon
        })
    return obj

#given number of pixels and zoom level, calculate the distance in latitudinal or longitudinal degrees
def calc_distance_degrees(distance,zoom):
    return (1.0*distance/256)*(360.0 / 2**zoom)

# get_map({'latitude': 25.7721638,'longitude': -80.2182310})
# print get_objects(15,{'latitude': 25.7721638,'longitude': -80.2182310})
