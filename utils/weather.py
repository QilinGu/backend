import pyowm
import os


'''
Get weather info - "rainy", "sunny", "cloudy", "snowy"
@param {dict} long_lat_dict
@returns {string} "rainy", "sunny", "cloudy", "snowy"
'''
def get_weather(long_lat_dict):
  owm_api = pyowm.OWM(os.getenv('WEATHER_API_KEY'))
  
  longitude = long_lat_dict.get("longitude", 0.0)
  latitude = long_lat_dict.get("latitude", 0.0)
  
  forecaster = owm_api.daily_forecast_at_coords(latitude, longitude)
  weather_code = (forecaster.get_forecast()
                  .get_weathers()[0]
                  .get_weather_code())
    
  if (weather_code >= 200 and weather_code <= 531):
    return "rainy"
  elif (weather_code >= 600 and weather_code <= 622):
    return "snowy"
  elif (weather_code >= 801 and weather_code <= 804):
    return "cloudy"
  else:
    return "sunny"
