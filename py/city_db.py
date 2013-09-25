# hack.sendgrid.com  @elbuo8 

from math import radians, cos, sin, asin, sqrt, log
import copy
import networkx as nx
import cPickle
import urllib2
import urllib
import json
import os
import fs_api
import google_api
import json
import urllib
import copy
from collections import Counter

GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?address=' 
CITIES_FILE = '../data/citydb.pkl'
GRAPH_FILE = '../data/graph.pkl'
THRESHOLD_KM = 800
CATEGORIES_FILE = '../data/categories.json'
CITY_TOP_PICKS = '../data/city_top_picks.pkl'


class CityDB:
  def __init__(self, do_load=False, city_limit=None):
    self.categories = {}  # id -> name
    self.name2category = {}
    self.load(do_load, city_limit)
    self.load_top_picks()
    self.load_category_tree()
    self.populate_vectors()
    self.build_city_graph()
  
  def find_by_name(self, city_name, allInfo=False):
    ''' Helper function for debugging '''
    match = filter(lambda c: c['city'] == city_name, self.cities)
    if len(match) == 0: return None
    
    if allInfo:
      return copy.deepcopy(match[0])
    else:
      obj = {'city': match[0]['city'], 'country': match[0]['country'],
              'lat': match[0]['lat'], 'lng': match[0]['lng']}
      if 'photo' in match[0]: obj['photo'] = match[0]['photo']
      return obj

  def load_top_picks(self):
    if os.path.exists(CITY_TOP_PICKS):
      with open(CITY_TOP_PICKS, 'r') as fin:
        self.top_picks = cPickle.load(fin)
    else:
      self.top_picks = {}

  def save_top_picks(self):
    with open(CITY_TOP_PICKS, 'w') as fout:
      cPickle.dump(self.top_picks, fout)

  

  def get_category_query_ancestor_id(self, category_id):
    cat_obj = self.cat_id2obj[category_id]
    while cat_obj and (not ('query' in cat_obj)):
      parent_id = self.cat_id2parentid[cat_obj["id"]]
      if parent_id:
        cat_obj = self.cat_id2obj[parent_id]
      else:
        cat_obj = None

    
    if cat_obj:
      return cat_obj["id"]
    else:
      return None

  def intersect_top_picks(self, category_ids, city):
    top_picks = self.get_top_pick_venues_for_city(city)
    category_ids = set(category_ids)
    return filter(lambda venue: len(category_ids.intersection([self.get_category_query_ancestor_id(c['id']) for c in venue['categories']])) > 0,
           top_picks)

  def get_city_interest_vector(self, city):
    top_picks = self.get_top_pick_venues_for_city(city)
    checkinsPerQueryId = Counter()
    for top_pick in top_picks:
      for cat in top_pick['categories']:
        catId = self.get_category_query_ancestor_id(cat['id'])
        if catId:
          checkinsPerQueryId[catId] += top_pick['stats']['usersCount']
    
    interest_vector = {}
    for k, v in checkinsPerQueryId.iteritems(): interest_vector[k] = v
    return interest_vector
    

  def populate_vectors(self):
    populated = False
    for city in self.cities:
      #if not 'vector' in city:
        populated = True
        city['vector'] = self.get_city_interest_vector(city)
    if populated: self.save()

  def fetch_next_100_top_picks(self, city):
    pass

  def get_top_pick_venues_for_city(self, city):
    #venues['response']['groups'][0]['items'][0]['venue']['stats']
    #{u'tipCount': 117, u'checkinsCount': 14673, u'usersCount': 5010}
    
    #venues['response']['groups'][0]['items'][0]['venue']['categories']
    if (city['city'], city['country']) in self.top_picks:
      return self.top_picks[(city['city'], city['country'])]
    
    results = []
    url = fs_api.url('/venues/explore', queryDict={'near': '%s, %s' % (city['city'], city['country']), 'section':'topPicks', 'limit':'100'})
    try:
      venues = self.read_json_at_url(url)
    except:
      #import pdb; pdb.set_trace()
      self.top_picks[(city['city'], city['country'])] = []
      return []

    if 'groups' in venues['response']:
      results = [item['venue'] for item in venues['response']['groups'][0]['items']]
    self.top_picks[(city['city'], city['country'])] = results
    self.save_top_picks()
    return results
  
  def translate_cat_keys(self, dictionary):
    translated_dict = {}
    for k, v in dictionary.iteritems():
      translated_dict[self.cat_id2name[k]] = v
    return translated_dict

  def load_category_tree(self):
    if os.path.exists(CATEGORIES_FILE):
      with open(CATEGORIES_FILE) as fin:
        self.root_categories = json.loads(fin.read())
        self.build_category_datastructs()
      return
    
      
    categories = self.read_json_at_url(fs_api.url('/venues/categories', {}))
    self.root_categories = []
    self.recursive_process_categories(self.root_categories, categories['response']['categories'])
    with open(CATEGORIES_FILE, 'w') as fout:
      fout.write(json.dumps(self.root_categories))

    self.build_category_datastructs()

  def recursive_process_categories(self, arrayToAddTo, categoriesToProcess):
    for category in categoriesToProcess:
      #import pdb; pdb.set_trace()
      category_obj = {'id': category['id'], 'name': category['name']}
      arrayToAddTo.append(category_obj)
      if 'categories' in category and len(category['categories']) > 0:
        category_obj['children'] = []
        self.recursive_process_categories(category_obj['children'], category['categories'])

  def recursive_build_category_datastructs(self, parent_id, children):
    for category in children:
      if 'query' in category:
        self.cat_query_categories.append(category)
      self.cat_id2obj[category['id']] = category
      self.cat_name2id[category['name']] = category['id']
      self.cat_id2name[category['id']] = category['name']
      self.cat_id2parentid[category['id']] = parent_id

      if 'children' in category:
        self.recursive_build_category_datastructs(category['id'], category['children'])

  def build_category_datastructs(self):
    # build the 2 dictionaries:
    self.cat_name2id = {}
    self.cat_id2obj = {}
    self.cat_id2name = {}
    self.cat_id2parentid = {}
    self.cat_query_categories = []
    
    self.recursive_build_category_datastructs(None, self.root_categories)


  def read_json_at_url ( self, url ):
    req = urllib2.Request( url )
    response = urllib2.urlopen(req)
    the_page = response.read()

    return json.loads( the_page )
    
  def coordinates_from_result( self, result ):
    geo = result['geometry']
    location = geo['location']
    
    return location['lng'], location['lat'] 

  def query_distance( self, source, destination ):
    url = google_api.distance_url( source, destination )
    print 'Querying: ' + url
    response = self.read_json_at_url( url )
    results = response['routes']

    return results
  
  def query_location(self, location_str ):
    url = google_api.coordinates_url( location_str ) 
    response = self.read_json_at_url( url )
    results = response['results']
    if len(results) == 0:
      print 'Error querying %s url: %s' % (location_str, url)

    return results

  def get_coordinates(self, city, country):
    results = self.query_location(city + ', ' + country)

    if len(results) > 0:
      lng, lat = self.coordinates_from_result( results[0] )
    else:
      lng, lat = [0, 0]

    return lng, lat

  def get_distance(self, source, destination ):
    results = self.query_distance( source, destination )

    if len(results) > 0:
      route = results[0]['legs'][0]
      distance = route['distance']['value']
      duration = route['duration']['value']
      
      return distance, duration
    else:
      return None

  def distance(self, origin, destination):
    lon1, lat1 = origin
    lon2, lat2 = destination

    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

  '''
  def distance(self, origin, destination):
    [lng1, lat1] = origin
    [lng2, lat2] = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlng = math.radians(lng2-lng1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
      * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d
  '''

  def build_city_graph(self):
    self.city_graph = nx.Graph()

    if os.path.exists(GRAPH_FILE):
      with open( GRAPH_FILE, 'r') as fin:
        data = cPickle.load(fin)
        self.city_graph = data['graph']

    for origin_city in self.cities:

      origin_label = (origin_city['city'],  origin_city['country'])

      weights = []
      for destination_city in self.cities:

        if origin_city == destination_city: continue

        destination_label = (destination_city['city'], destination_city['country'])

        origin = [origin_city['lng'], origin_city['lat']]
        destination = [destination_city['lng'], destination_city['lat']]
        distance = self.distance(origin, destination)

        if distance < THRESHOLD_KM:
          weights.append((distance, destination_label))
          self.city_graph.add_edge( origin_label, destination_label, weight=distance )

        sorted_weights = sorted(weights, key=lambda edge: edge[0])
        
        if len(sorted_weights) > 5:
          sorted_weights = sorted_weights[0:5]
      
        origin_city['nearby_vector'] = copy.deepcopy(origin_city['vector'])

        for edge in sorted_weights:
          dest = edge[1]
          dest_city = self.city_in_db(dest[0], dest[1])

          for key in dest_city['vector']:
            if key in origin_city['nearby_vector']:
              origin_city['nearby_vector'][key] += dest_city['vector'][key]
            else:
              origin_city['nearby_vector'][key] = dest_city['vector'][key]

    self.save()
    self.save_graph()

  def dot_product(self,vector_1, vector_2):
    dot_prod = 0
    for key in vector_1:
      if key in vector_2:
        dot_prod += vector_1[key] * vector_2[key]

    return dot_prod


  def find_matching_cities(self, user_vector, limit=50, duration=14):

    dot_prods = []

    vector_type = 'nearby_vector'

    for city in self.cities:
      dot_prod = 0
      for key in city[vector_type]:
        if key in user_vector:
          dot_prod += log(city[vector_type][key]) * user_vector[key]
      dot_prods.append((dot_prod, (city['city'], city['country'])))

    sorted_cities = sorted(dot_prods, key=lambda prod: -1 * prod[0])

    if len(sorted_cities) > limit:
      sorted_cities = sorted_cities[:limit]

    return sorted_cities

  def find_path(self, user_vector, city_name, country, path, remaining_duration):
    path.append((city_name, country))
    if remaining_duration < 48:
      return path
    best_dot_prod = -1
    best_city = None

    for node in self.city_graph.neighbors((city_name, country)):
      city = self.city_in_db(node[0], node[1])
      dot_prod = self.dot_product(user_vector, city['vector'])
      if dot_prod > best_dot_prod and (city['city'], city['country']) not in path:
        best_dot_prod = dot_prod
        best_city = city
    if best_city:
      weight = self.city_graph.edge[(city_name, country)][(best_city['city'], best_city['country'])]['weight'] / 80
      return self.find_path(user_vector, best_city['city'], best_city['country'], path, remaining_duration - 48 - weight) 
    else:
      return path
                                                          

  def save_graph(self):
    data = {'graph': self.city_graph}
    with open(GRAPH_FILE, 'w') as fout:
      cPickle.dump(data, fout)

  def load(self, fetch_new=True, limit=None):
    ''' loads cities from file (or create file if does not exist)'''
    self.cities = []
    #self.load_categories()
    if os.path.exists(CITIES_FILE):
      with open(CITIES_FILE, 'r') as fin:
        data = cPickle.load(fin)
        self.cities = data['cities']
        self.categories = data['categories']
        self.name2category = {}
        for k,v in self.categories.iteritems(): self.name2category[v] = k
      #return
    
    self.city_index = {}
    for c in self.cities:
      self.city_index[(c['city'], c['country'])] = c

    if not fetch_new: return
    # Otherwise, load the cities
    i = 0
    with open('../data/cities.txt', 'r') as fin:
      line = fin.readline()
      while line and (limit == None or i < limit):
        i = i + 1
        print i
        line = line.rstrip()
        city, country = line.split(' @ ')

        if not self.city_in_db(city, country):
          self.add_city_to_db(city, country)
          self.save()
        
        line = fin.readline()

    # Save
    self.save()

  def city_in_db(self, city, country):
    for c in self.cities:
      #import pdb; pdb.set_trace()
      if city == c['city'] and country == c['country']:
        return c

    return False

  def add_city_to_db(self, city, country):
    lng, lat = self.get_coordinates(city, country)    
    city_obj = {"city": city, "country": country, "lat": lat, "lng": lng}
    self.cities.append(city_obj)
        
    #city_obj["poi"] = self.get_pois(city, country)
  '''
  def load_categories(self):
    self.categories = {}
    self.name2category = {}
    with open('../data/printed_categories.txt', 'r') as fin:
      line = fin.readline()
      while line:
        if line[0] == '\t':
          line = fin.readline()
          continue
        line = line.rstrip()
        parts = line.split(' ')
        
        self.categories[parts[-1]] = ' '.join(parts[0:-1])
        self.name2category[' '.join(parts[0:-1])] = parts[-1]
        line = fin.readline()
  '''
  def get_pois(self, city, country):
    cat_places = {}
#    for categoryId, categoryName in self.categories.iteritems():

    # url = fs_api.url(queryDict={'near': '%s, %s' % (city, country), 'categoryId':categoryId,
    url = fs_api.url(queryDict={'near': '%s, %s' % (city, country), 'section':'topPicks'})
    data = json.loads( urllib.urlopen(url).read() )
    if not 'groups' in data['response']:
      print 'failed to load for url %s' % url
      return

    items = data['response']['groups'][0]['items']
#     cat_places[categoryId] = []
    for item in items:
      # Find the parent
      #import pdb; pdb.set_trace()

      if len(item['categories']) == 0: 
        continue

      for parent in item['categories'][0]['parents']:
        if parent in self.name2category:
          parent_id =  self.name2category[parent]
          if not parent_id in cat_places: cat_places[parent_id] = []

      categoryId = item['categories'][0]['id']

      cat_places[parent_id].append({
            'name': item['name'], 
            'category': categoryId,
            'lat': item['location']['lat'],
            'lng': item['location']['lng'],
            'stats': item['stats'],
          })

    for parent_id in cat_places.iterkeys():
      cat_places[parent_id] = sorted(cat_places[parent_id], key=lambda x: -1 * x['stats']['usersCount'])
    
    return cat_places

  def save(self):
    ''' dumps cities to file '''
    data = {'categories': self.categories, 'cities': self.cities}
    with open(CITIES_FILE, 'w') as fout:
      cPickle.dump(data, fout)


if __name__ == '__main__':
  city_db = CityDB()
  import time
  import pictures
  for city in city_db.cities:
    time.sleep(0.3)
    if 'photo_url' not in city:
      try:
        city['photo_url'] = pictures.get_picture(city['city'])
      except:
        pass

  city_db.save()

