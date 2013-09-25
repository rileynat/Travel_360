
import json
from flask import Flask, url_for, send_file, Response, request
from city_db import CityDB

CITY_DB = CityDB()
app = Flask(__name__)

@app.route("/interests")
def interests():
  interests = [(c['id'], c['name']) for c in CITY_DB.cat_query_categories]
  return Response(json.dumps(interests, separators=(',',':')), mimetype='application/json')

@app.route("/all_city_locations")
def all_city_locations():
  cities = [{'city': c['city'], 'country': c['country'], 'lat': c['lat'], 'lng': c['lng']} \
             for c in CITY_DB.cities]
  edges = []
  for entry in CITY_DB.city_graph.edges(): 
    coord_a = {'lat':CITY_DB.city_index[entry[0]]['lat'], 'lng':CITY_DB.city_index[entry[0]]['lng']}
    coord_b = {'lat':CITY_DB.city_index[entry[1]]['lat'], 'lng':CITY_DB.city_index[entry[1]]['lng']}
    edges.append((coord_a, coord_b))
  return Response(json.dumps({'cities': cities, 'edges': edges} , separators=(',',':')), mimetype='application/json')


@app.route("/search")
def search():
  cats = request.args.get('categories')
  dateFrom = request.args.get('from')
  dateTo = request.args.get('to')

  user_vector = {}
  for cat in cats.split(','):
    user_vector[cat] = 1

  matching_cities = CITY_DB.find_matching_cities(user_vector)
  
  cities = [{'city': c[1][0], 'country': c[1][1]} for c in matching_cities]
  
  #import pdb; pdb.set_trace()

  itineraries = []
  for i in range(10):
    path = CITY_DB.find_path(user_vector, cities[i]['city'], cities[i]['country'], [], 14*24)
    itin = {'headline': 'Vacation %d' % (i + 1), 'destinations': [CITY_DB.find_by_name(name) for name, country in path]}
    itineraries.append(itin)

  ''' 
  itin2 = {'headline': 'Europe / Former Yugoslavia', 'destinations':
            [CITY_DB.find_by_name('Vienna'), CITY_DB.find_by_name('Zagreb'),
           CITY_DB.find_by_name('Belgrade')]}
  '''
  return Response(json.dumps({'itineraries': itineraries}), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)




