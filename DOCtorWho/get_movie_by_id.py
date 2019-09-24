import pprint
import pickle
import sys

moviesFile = open('data/movies.pickled', mode= "rb")
movies = pickle.load(moviesFile)
pprint.pprint (movies[sys.argv[1]])

