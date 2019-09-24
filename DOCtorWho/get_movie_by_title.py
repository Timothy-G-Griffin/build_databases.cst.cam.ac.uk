import pprint
import pickle
import sys

moviesFile = open('data/movies.pickled', mode= "rb")
movies = pickle.load(moviesFile)
title = sys.argv[1]
movie = {} 
for movie_id in movies.keys():
    if movies[movie_id]['title'] == title:
        movie = movies[movie_id]

pprint.pprint (movie)

