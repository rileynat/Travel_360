import csv
import city

def main(): 
  cities = []
  with open('destinations.csv', 'rb') as csvfile: 
    r = csv.reader(csvfile)
    for row in r:
      index = 0
      for i in range((len(row))/2): 
        new_city = city.City(row[i], row[i+1])
        cities.append(new_city)
        index = index + 2
        

if __name__ == "__main__": 
    main()
