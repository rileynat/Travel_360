import json
from city import City
from fs_api import url
import urllib2

def serialize_cities():
    f = open('../data/small.txt', 'r')
    for line in f:
        a = line.split()
        city = a[0]
        country = a[1]

        newCity = City(city, country)

        query = 'arts'
        limit = '10'

        my_url = url('/venues/explore', {'near':city +', ' + country, 'section':query, 'limit':limit})
        result = urllib2.urlopen(my_url).read()

        newCity.activities.append( json.loads(result) )

serialize_cities()
