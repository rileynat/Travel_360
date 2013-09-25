import urllib

API_key = 'eda991b43475b115a2d2bbecae1ebf5f'

def url(from_airport='LGA', to='DTW', departure_date='2013-9-20', return_date='2014-1-1', num_adults=1, num_children=0, num_infants=0, cabin_type='Economy'):
    full_url = 'https://api.cleartrip.com/air/1.0/search?from=%s&to=%s&depart-date=%s&return-date=%s&adults=%d&children=%d&infants=%d&cabin-type=%s' % (from_airport, to, departure_date, return_date, num_adults, num_children, num_infants, cabin_type)

    return full_url


