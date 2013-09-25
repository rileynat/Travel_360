import requests
import json


def get_picture(city_name): 
  """Function that returns the URL of the first google image search result for the given city name."""
  r = requests.get('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s'%(city_name))
  response = r.json
  img_url =  response['responseData']['results'][0]['unescapedUrl']
  return img_url

def main():
  get_picture('hi')

if __name__ == "__main__": 
    main()
