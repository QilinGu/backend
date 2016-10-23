from flask import Flask, g, request, json
from services import auth, account, maprender
from utils import weather
import decorators


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home_route():
  return json.jsonify({
    "status": 200,
    "message": "Roam Backend API v1"
  })

@app.route('/signup', methods=['POST'])
def signup_route():
  request_dict = request.get_json(force=True, silent=True)
  username = request_dict.get("username")
  password = request_dict.get("password")
  class_id = request_dict.get("class_id")
  
  try:
    auth.signup(username, password, class_id)
  except:
    response = json.jsonify({
      "status": 400,
      "message": "failure"
    })
    response.status_code = 400
    return response
  
  return json.jsonify({
    "status": 200,
    "message": "success"
  })

@app.route('/login', methods=['POST'])
def login_route():
  request_dict = request.get_json(force=True, silent=True)
  username = request_dict.get("username")
  password = request_dict.get("password")
  
  jwt_token = None
  try:
    jwt_token = auth.login(username, password)
  except BaseException as e:
    response = json.jsonify({
      "status": 400,
      "message": str(e)
    })
    response.status_code = 400
    return response
  
  if jwt_token is None:
    response = json.jsonify({
      "status": 400,
      "message": "user doesn't exist or wrong password"
    })
    response.status_code = 400
    return response
    
  return json.jsonify({
    "status": 200,
    "message": jwt_token
  })

@app.route('/user/me/account', methods=['GET', 'POST'])
@decorators.auth_protected
def user_account_route():
  jwt_token = g.jwt_token
  user_id = jwt_token.get("id")
  
  if user_id is None:
    response = json.jsonify({
      "status": 400,
      "message": "user_id is required in JWT token"
    })
    response.status_code = 400
    return response
  
  if request.method == "GET":
    user_info = account.get_user(user_id)
    if user_info is None:
      response = json.jsonify({
        "status": 400,
        "message": "user does not exist"
      })
      response.status_code = 400
      return response
    
    return json.jsonify(user_info)
    
  if request.method == "POST":
    request_dict = request.get_json(force=True, silent=True)
    if not isinstance(request_dict, dict):
      response = json.jsonify({
        "status": 400,
        "message": "request_body not obtained"
      })
      response.status_code = 400
      return response
    
    account.update_user(user_id, request_dict)
    
    return json.jsonify({
      "status": 200,
      "message": "user succesfully updated"
    })

@app.route('/maprender', methods=['POST'])
@decorators.auth_protected
def maprender_route():
  request_dict = request.get_json(force=True, silent=True)
  if not isinstance(request_dict, dict):
    response = json.jsonify({
      "status": 400,
      "message": "request_body not obtained"
    })
    response.status_code = 400
    return response
  
  x = request_dict.get("x", 0)
  y = request_dict.get("y", 0)
  center = request_dict.get("center", {})
  
  res_map = maprender.get_new_map(x, y, center)
  render_objects = maprender.get_objects(15, center)
  weather_info = weather.get_weather()
  
  return json.jsonify({
    "image_url": res_map, 
    "weather": weather_info, 
    "render_objects": render_objects 
  })
