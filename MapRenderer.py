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

key = open('config.txt').read()
def map_render(location, orientation):
    lat  = location['latitude']
    lon = location['longitude']
    URL = "https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=15&size=640x640&style=feature:landscape.man_made|color:0xa9a9a9&style=feature:all|element:labels|visibility:off&style=feature:road|color:0x654321&style=feature:poi.business|color:0x186842&style=feature:poi.attraction|color:0xff0000&style=feature:poi.government|color:0x00ff00&style=feature:poi.medical|color:0x0000ff&style=feature:poi.park|color:0x000000&style=feature:poi.place_of_worship|color:0x631355&style=feature:poi.school|color:0x584788&style=feature:poi.sports_complex|color:0x797923&key=%s" % (lat, lon, key)
    response = requests.get(URL)
    print URL
    img = Image.open(StringIO(response.content))
    img = img.crop((0,0,640,615)).rotate( orientation, expand=1 )
    img.save("map2.png")

map_render({'latitude': 25.7721638,'longitude': -80.2182310}, 0)
