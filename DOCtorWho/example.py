import json
import pprint
import pickle

moviesFile = open('IMDb_json/movies.pickled', mode= "rb")
peopleFile = open('IMDb_json/people.pickled', mode= "rb")

movies = pickle.load(moviesFile)
people = pickle.load(peopleFile)

print ('Test Movies')
pprint.pprint (movies["tt1045658"])
print ('Test People')
pprint.pprint (people['nm2225369'])
