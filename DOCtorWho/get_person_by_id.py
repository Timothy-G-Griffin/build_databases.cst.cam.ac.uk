import pprint
import pickle
import sys

peopleFile = open('data/people.pickled', mode= "rb")
people = pickle.load(peopleFile)
pprint.pprint (people[sys.argv[1]])

