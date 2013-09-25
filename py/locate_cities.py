
def locate_cities(cities):
  # cities are pairs of (city name, country name)
  # https://maps.googleapis.com/maps/api/geocode/json?address=Chicago,%20US&sensor=false
  locations = open('data/locate_cities.py').read().split(' @ ')
  cities = []
  countries = []
  for i, entry in enumerate(locations): 
    if i%2: 
      cities += entry
    else: 
      countries += entry
   https://maps.googleapis.com/maps/api/geocode/json?address=Chicago,%20US&sensor=false
  



