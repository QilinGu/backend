# def maprender({lat,long}, degreesFromNorth)
# returns styled image
#
# 25.7721638,-80.2182310
import urllib
from PIL import Image
import requests
from StringIO import StringIO

key = open('config.txt').read()
def map_render(location, orientation):
    lat  = location['latitude']
    lon = location['longitude']
    URL = "https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=15&size=600x600&key=%s" % (lat, lon, key)
    response = requests.get(URL)
    print URL
    img = Image.open(StringIO(response.content))
    img = img.rotate( orientation, expand=1 )
    img.save("map2.png")

map_render({'latitude': 25.7721638,'longitude': -80.2182310}, 90)
