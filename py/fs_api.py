import urllib

CLIENT_ID = '2C2OMEYXHWI5LSAJ4EMLFMVYEWVOMH5B5NS50T3GB1UIT354'
SECRET = 'QO5WJBRCUBWMRVWWNFIWHQHSFSDCQWKGFJACSJ0MEO22LSPY'

def url(endpoint='/venues/explore', queryDict={'near': 'Chicago, IL', 'query': 'night club'}):
  full_url = 'https://api.foursquare.com/v2%s?client_id=%s&client_secret=%s' % (
                endpoint, CLIENT_ID, SECRET)
  
  for k, v in queryDict.iteritems():
    full_url += '&%s=%s' % (k, urllib.quote(v))
    
  return full_url
  


