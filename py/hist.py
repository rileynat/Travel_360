from city_db import CityDB
from collections import Counter

db = CityDB(False)


def sort_histogram(histogram):
  return sorted(histogram.items(), key=lambda (cat_id, count): -1 * count)


for city in db.cities:
  placesPerCat = Counter()
  checkinsPerCat = Counter()
  for category_id, place_list in city['poi'].iteritems():
    placesPerCat[category_id] += len(place_list)
    usersCount = [ place['stats']['usersCount'] for place in place_list ]
    checkinsPerCat[category_id] += sum(usersCount)
  print ''
  print "%s @ %s CHECKINS(" % (city['city'], city['country'] ),
  #for cat_id, count in sort_histogram(placesPerCat)[:5]:
  #  print ' %s:%i' % (db.categories[cat_id], count ),
  
  for cat_id, count in sort_histogram(checkinsPerCat)[:5]:
    print ' %s:%i' % (db.categories[cat_id], count ),
  
  print ')'



