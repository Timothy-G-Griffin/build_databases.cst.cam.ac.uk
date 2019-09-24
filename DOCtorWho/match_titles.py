import pprint
import pickle
import sys
import re 

moviesFile = open('data/movies.pickled', mode= "rb")
movies = pickle.load(moviesFile)
regexp = sys.argv[1]
for movie_id in movies.keys():
    title = movies[movie_id]['title']
    m = re.match(regexp, title) 
    if m is not None:
        pprint.pprint ({'title' : title, 'movie_id' : movie_id})

