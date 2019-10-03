import sys     # talk to the operating system 
import os.path # manipulate paths to files, directories 
import pickle  # read/write pickled python dictionaries 
import pprint  # pretty print JSON

data_dir = sys.argv[1] # directory of data 
title    = sys.argv[2] # movie title 

# use os.path.join so that path works on both Windows and Unix 
movies_path = os.path.join(data_dir, 'movies.pickled')

# open the movies dictionary file and un-pickle it 
moviesFile = open(movies_path, mode= "rb")
movies = pickle.load(moviesFile)

# initialise output movie 
the_movie = {} 

# iterate through all the keys of the movie dictionary 
# looking for one with the right title 
for movie_id in movies.keys():
    if movies[movie_id]['title'] == title:
        the_movie = movies[movie_id]
        break 
  
pprint.pprint (the_movie)

