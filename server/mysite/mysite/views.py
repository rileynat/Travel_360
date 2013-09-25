
from  django.http import HttpResponse

import json

def send_file(filename):
	with open('static/' + filename) as fin:
		return HttpResponse(fin.read())

def index(request):
	return send_file('demo.html')

def search(request):
	obj = [
		{'title': 'Eastern Europe',
		 'description':'nasty stuff',
		 'itinerary':[
		 	{'name': 'Berlin'},
		 	{'name': 'Prague'},
		 	{'name': 'Vienna'},
		 ]},

		{'title': 'East Coast (US)',
		 'description':'nasty stuff',
		 'itinerary':[
		 	{'name': 'Berlin'},
		 	{'name': 'Prague'},
		 	{'name': 'Vienna'},
		 ]},

	]

	return HttpResponse(json.dumps(obj), mimetype="application/json")
