import urllib

def url(origin_lat=0, origin_long=0, dest_lat=0, dest_long=0, sensor='false', mode='driving', departure_date=1379755062, arrival_date=1379841462):
    full_url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%f,%f&destination=%f,%f&sensor=%s&mode=%s' % (origin_lat, origin_long, dest_lat, dest_long, sensor, mode)

    if mode == 'transit':
        full_url += '&%f&%f' % (departure_date, arrival_date)

    return full_url
