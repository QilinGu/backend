import functools
import flask
import utils
import os


JWT_TOKEN_SECRET = os.getenv("JWT_TOKEN_SECRET")


'''
Auth decorator
@param {Function} decorated_function
'''
def auth_protected(decorated_function):
  @functools.wraps(decorated_function)
  def decorator(*args, **kwargs):
    auth_header = flask.request.headers.get('Authorization', None)
    if auth_header is None:
      response = flask.json.jsonify({
        "status": 400,
        "message": "JWT Token required for this route"
      })
      response.status_code = 400
      return response
    
    try:
      token = utils.auth.auth_token_decode(
        JWT_TOKEN_SECRET, 
        utils.auth.authorization_header_token(
          auth_header
        )
      )
      setattr(flask.g, "jwt_token", token)
    except (TypeError, ValueError) as e:
      response = flask.json.jsonify({
        "status": 400,
        "message": str(e)
      })
      response.status_code = 400
      return response
    
    return decorated_function(*args, **kwargs)
  return decorator
