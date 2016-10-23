# poi.attraction selects tourist attractions.  0x186842
# poi.business selects businesses.   0xff0000
# poi.government selects government buildings. 0x00ff00
# poi.medical selects emergency services, including hospitals, pharmacies, police, doctors, and others. 0x0000ff
# poi.park selects parks. 0x000000
# poi.place_of_worship selects places of worship, including churches, temples, mosques, and others. 0x631355
# poi.school selects schools. 0x584788
# poi.sports_complex selects sports complexes.0x797923
from flask import Flask, request, json
app = Flask(__name__)
import maprender



@app.route("/")
def hello():
    return "Hello World!"


#Function to return nearby maps based off of last map's center
@app.route('/maprender', methods=['POST'])
def update_map():
    obj = json.loads(request.data)
    x = obj['x']
    y = obj['y']
    center = obj['center']
    res_map = maprender.get_new_map(x , y, center)
    return json.jsonify({"image_url": res_map})



loc = {'latitude': 25.7721638,'longitude': -80.2182310}
#map_render(loc)
#map_render2({'latitude': (25.7721638),'longitude': (-80.2182310 - calc_distance_degrees(640,16))}, 0)
#print update_map("top-left", loc)
if __name__ == "__main__":
    app.run()
