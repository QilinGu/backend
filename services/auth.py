import utils
import os
import datetime

'''
Validate login provided username and password and 
  return JWT token on success
@param {string} username
@param {string} password
@returns {string|None} JWT token on success, None on failure
'''
def login(username, password):
  if not isinstance(username, basestring):
    raise TypeError("username must be a string")
  if not isinstance(password, basestring):
    raise TypeError("password must be a string")
  
  result_list = utils.db.relational_query(
    """
    SELECT id, username, password 
    FROM users
    WHERE username=%s
    """,
    [username]
  )
  if len(result_list) == 0:
    return None
  
  user_id = result_list[0][0]
  username = result_list[0][1]
  hashed_password = result_list[0][2]
  if not utils.auth.hash_compare(password, hashed_password):
    return None
    
  jwt_token_secret = os.getenv("JWT_TOKEN_SECRET", None)
  return utils.auth.auth_token_encode(jwt_token_secret, {
    "id": user_id, 
    "username": username
  })


'''
Signs a user up
@param {string} username
@param {string} password
@param {int} class_id
@returns {bool} TRUE on success, FALSE otherwise
'''
def signup(username, password, class_id):
  if not isinstance(username, basestring):
    raise TypeError("username must be a string")
  if not isinstance(password, basestring):
    raise TypeError("password must be a string")
  if not isinstance(class_id, int):
    raise TypeError("class_id must be an int")
    
  hashed_password = utils.auth.hash_password(password)
  
  try:
    utils.db.relational_query(
      """
      INSERT INTO users (username, password, class_id, 
        created_at, xp, hp) 
      VALUES (%s, %s, %s, %s, 0, 0);
      """,
      [username, hashed_password, class_id, datetime.datetime.now()]
    )
  except BaseException:
    return False
  
  return True
  