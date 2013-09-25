import requests
import city_db
import cPickle
import os
import time

WEATHER_CACHE_FILE = '../data/weather.pkl'



class Weatherground:



    def __init__(self):
        self.city_db = city_db.CityDB()
        self.cache = {}  # (city, country, year, month, day) => temperature
        self.string_array = ['6f0099417173bd3a', '7f94e9a029db6647', 'a4c487b1a7684f5e', 'c23912d2f22b60a2', 'd5fd5c01532ee6b2', '5466aeada237f339', '452ceaac4d9108e3', '1f69cdc102ef4916','010ce6e0434b61e6','b959a8347d6e88a6','76d11f55ac3f532a','7b5d0087340f7946','14b0c54ca8eaa89a','9a43fd3bc52ae4a6','bc9fbd0a246f151c']
        self.array_index = 0
        if os.path.exists(WEATHER_CACHE_FILE):
            with open(WEATHER_CACHE_FILE,'r') as fin:
                self.cache = cPickle.load(fin)

    def get_temp(self, city='Sydney', country='Austrailia', year=2013, month=8, day=1):
        cache_key = (city, country, year, month, day)
        if cache_key in self.cache and self.cache[cache_key] != 65: return self.cache[cache_key]
        
        temperature = self.get_city_history_temperature( city, country, year, month, day)
        self.cache[cache_key] = temperature
        with open(WEATHER_CACHE_FILE, 'w') as fout: cPickle.dump(self.cache, fout)
        

    def populate_all_cities(self):
        for city in self.city_db.cities:
            if city['country'][0] is 'U':
                if city['country'][5] is 'd':
                    if city['country'][7] is 'S':
                        c = city_db.CityDB()
                        j = c.query_location(city['city'] + ', ' + city['country'])
                        city['state'] = j[0]['address_components'][2]['short_name']
                        for month in range(1, 13):
                            self.get_temp(city['city'], city['state'], 2012, month)
                        self.array_index = (self.array_index + 1) % 15
#                        print '  incremented keys'
                        self.city_db.save()

    def populate_state_names_with_temp(self):
        for city in self.city_db.cities:
            if city['country'] == 'United States':
                c = city_db.CityDB()
                j = c.query_location(city['city'] + ', ' + city['country'])
                city['state'] = j[0]['address_components'][2]['short_name']
                for month in range(1, 13):
                    self.get_temp(city['city'], city['state'], 2012, month)
            for month in range(1,13):
                print month
                self.get_temp(city['city'], city['country'], 2012, month, 1)
            self.array_index = (self.array_index + 1) % 15
            #print '  incremented keys'
            #time.sleep(10)
        self.city_db.save()

    def get_city_history_temperature(self, city='Sydney', country='Austrailia', year=2013, month=8, day=1):
        incrementer = 4
        total = 0.0
        for x in range(0, incrementer+1) :
            full_url = 'http://api.wunderground.com/api/bc9fbd0a246f151c/history_%d%02d%02d/q/%s/%s.json' % (self.string_array[self.array_index] ,year - x, month, day, country, city)
            r = requests.get(full_url)
            response = r.json()
            try:
                total += float(response['history']['dailysummary'][0]['meantempi'])
            except:
                print 'error %s %s' % (city, country)
                return -1
        return total/incrementer

    
