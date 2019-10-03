import pprint
import pickle
import sys
import json

peopleFile = open('data/people.pickled', 'rb')
people = pickle.load(peopleFile)
pprint.pprint (people[sys.argv[1]])

