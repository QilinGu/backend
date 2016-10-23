import jwt
import bcrypt


'''
Obtains the JSON token stored on the Authorization Header 
  and returns back that stored JSON token
@param authorization_header {string}
@returns {string}
'''
def authorization_header_token(authorization_header):
  if isinstance(authorization_header) is not basestring:
    raise TypeError("authorization_header must be a string")
  
  auth_header_token = authorization_header.replace('Bearer ', '')
  if not auth_header_token:
    raise ValueError("authorization_header is empty")
  
  return auth_header_token


'''
Encodes the provided dict into a JWT Token. The payload 
  will be public information - secret key is only used to ensure 
  that when we receive the token back, it hasn't been mutated 
  without our explicit knowledge (use of that secret_key)
@param secret_key {string}
@param payload {dict}
@returns {string}
'''
def auth_token_encode(secret_key, payload_dict):
  if isinstance(secret_key) is not basestring:
    raise TypeError("secret_key must be a string")
  if isinstance(payload_dict) is not dict:
    raise TypeError("payload_dict must be a dict")
  
  return jwt.encode(payload_dict, secret_key, algorithm='HS256')


'''
Decodes the provided JWT Token into a dict. The secret key 
  is used for validation of token signature
@param secret_key {string}
@param encoded_string {string}
@returns {string}
'''
def auth_token_decode(secret_key, encoded_string):
  if isinstance(secret_key) is not basestring:
    raise TypeError("secret_key must be a string")
  if isinstance(encoded_string) is not basestring:
    raise TypeError("encoded_string must be a string")
  
  return jwt.decode(encoded_string, secret_key)


'''
Hash a provided password
@param {string} password
@returns {string}
'''
def hash_password(password):
  return bcrypt.hashpw(password, bcrypt.gensalt(14))


'''
Compare a password to a hashed password
@param {string} password
@param {hashed_password}
@returns {boolean} TRUE if match, FALSE otherwise
'''
def hash_compare(password, hashed_password):
  return bcrypt.hashpw(password, hashed_password) == hashed_password
