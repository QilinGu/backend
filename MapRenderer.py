# def maprender({lat,long}, degreesFromNorth)
# returns styled image
#
# 25.7721638,-80.2182310
#
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

key = open('config.txt').read()
def map_render(location):
    #Get latitude, longitude from location dict
    lat  = location['latitude']
    lon = location['longitude']

    #Get and style static google map from api
    URL = "https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=16&size=640x640&maptype=terrain&style=feature:landscape.man_made|color:0x222211&style=feature:all|element:labels|visibility:off&style=feature:road|color:0x654321&style=feature:poi.business|color:0x186842&style=feature:poi.attraction|color:0xff0000&style=feature:poi.government|color:0x00ff00&style=feature:poi.medical|color:0x0000ff&style=feature:poi.park|color:0x000000&style=feature:poi.place_of_worship|color:0x631355&style=feature:poi.school|color:0x584788&style=feature:poi.sports_complex|color:0x797923&key=%s" % (lat, lon, key)
    #Save as image file
    response = requests.get(URL)
    print URL
    img = Image.open(StringIO(response.content))
    img = img.crop((0,0,640,615))
    t = time.time()
    time_string = "%f" % t
    mult = len(time_string.split('.')[1])
    map_name = "./maps/map_%d.png" % (t * 10**mult)
    img.save(map_name)

def update_map(where , prev):
    add_lon = 0
    add_lat = 0
    if where == "top":
        add_lat = calc_distance_degrees(615,16)
    elif where == "bottom":
        add_lat = calc_distance_degrees(615,16) * -1
    elif where == "left":
        add_lon = calc_distance_degrees(640,16) * -1
    elif where == "right":
        add_lon = calc_distance_degrees(640,16)
    elif where == "top-right":
        add_lat = calc_distance_degrees(615,16)
        add_lon = calc_distance_degrees(640,16)
    elif where == "top-left":
        add_lat = calc_distance_degrees(615,16)
        add_lon = calc_distance_degrees(640,16) * -1
    elif where == "bottom-left":
        add_lat = calc_distance_degrees(615,16) * -1
        add_lon = calc_distance_degrees(640,16) * -1
    elif where == "bottom-right":
        add_lat = calc_distance_degrees(615,16) * -1
        add_lon = calc_distance_degrees(640,16) * -1
    map_render2({'latitude': (prev['latitude'] + add_lat),'longitude': (prev['longitude'] + add_lon)})

def map_render2(location):
    lat  = location['latitude']
    lon = location['longitude']
    URL = "https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=16&size=640x640&maptype=terrain&style=feature:landscape.man_made|color:0x222211&style=feature:all|element:labels|visibility:off&style=feature:road|color:0x654321&style=feature:poi.business|color:0x186842&style=feature:poi.attraction|color:0xff0000&style=feature:poi.government|color:0x00ff00&style=feature:poi.medical|color:0x0000ff&style=feature:poi.park|color:0x000000&style=feature:poi.place_of_worship|color:0x631355&style=feature:poi.school|color:0x584788&style=feature:poi.sports_complex|color:0x797923&key=%s" % (lat, lon, key)
    response = requests.get(URL)
    print URL
    img = Image.open(StringIO(response.content))
    img = img.crop((0,0,640,615))
    t = time.time()
    time_string = "%f" % t
    mult = len(time_string.split('.')[1])
    map_name = "./maps/map2_%d.png" % (t * 10**mult)
    img.save(map_name)

def calc_distance_degrees(distance,zoom):
    print (1.0*distance/256)*(360.0 / 2**zoom)
    return (1.0*distance/256)*(360.0 / 2**zoom)


loc = {'latitude': 25.7721638,'longitude': -80.2182310}
map_render(loc)
#map_render2({'latitude': (25.7721638),'longitude': (-80.2182310 - calc_distance_degrees(640,16))}, 0)
# update_map("left", loc)
