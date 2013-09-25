def csv_to_delimed_cities( source, destination ):
	l = open( source ).read().split(', ')

	locations = l

	cities = [(locations[2*i], locations[2*i+1]) for i in xrange(len(locations)/2)]

	fout = open( destination, 'w')
	for city, country in cities: fout.write('%s @ %s\n' % (city, country))

	fout.close()

source = '../data/destinations.csv'
destination = '../data/cities.txt'

csv_to_delimed_cities( source, destination )
