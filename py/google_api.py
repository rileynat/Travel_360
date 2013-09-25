import urllib

GOOGLE_API_URL = 'http://maps.googleapis.com/maps/api'

def coordinates_url( location_str ):
  return url(endpoint='/geocode', queryDict={'address': location_str, 'sensor': 'false'})

def distance_url( source, destination ):
  return url(endpoint='/directions', queryDict={'origin': source, 'destination': destination, 'sensor': 'false'})
  

def url(endpoint='/directions', output='/json', queryDict={}):
  full_url = GOOGLE_API_URL + endpoint + output + '?'
  
  for k, v in queryDict.iteritems():
    full_url += '&%s=%s' % (k, urllib.quote(v))
    
  return full_url
  





