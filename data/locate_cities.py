
l = open('destinations.csv').read().split(', ')

locations = l

cities = [(locations[2*i], locations[2*i+1]) for i in xrange(len(locations)/2)]

fout = open('cities.txt', 'w')
for city, country in cities: fout.write('%s @ %s\n' % (city, country))

fout.close()

