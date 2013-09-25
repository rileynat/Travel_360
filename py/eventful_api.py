import urllib

APPLICATION_KEY = 'vS74NdgtNvZMfDh3'

def url(city='Chicago', country='United States', param_dict={'count_only': 'true' }):
    city = city.replace(" ", "+")
    country = country.replace(" ", "+")
    full_url = 'http://api.eventful.com/rest/events/search?app_key=%s&%s,%s&date=Future' % (APPLICATION_KEY, city, country)
    
    for k, v in param_dict.iteritems():
        full_url += '&%s=%s' % (k, urllib.quote(v))

    return full_url
