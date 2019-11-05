
# This will be the common prelude to all of our queries. 

import sys     # talk to the operating system 
import os.path # manipulate paths to files, directories 
import pickle  # read/write pickled python dictionaries 
import pprint  # pretty print JSON

data_dir = sys.argv[1] # directory of data 

# use os.path.join so that path works on both Windows and Unix 
movies_path = os.path.join(data_dir, 'movies.pickled')
people_path = os.path.join(data_dir, 'people.pickled')

# open data dictionary files and un-pickle them 
moviesFile = open(movies_path, mode= "rb")
movies = pickle.load(moviesFile)

peopleFile = open(people_path, mode= "rb")
people = pickle.load(peopleFile)

############### EXAMPLE #######################

# For tick 2 exercise2b we had to write a query something like this
# 
# match (m:Movie{title : 'The Matrix Reloaded'}) 
#        <-[r1:ACTED_IN]- (p) -[r2:ACTED_IN]->
#       (n:Movie {title : 'John Wick'}) 
# return p.name as name, r1.roles as roles1, r2.roles as roles2 
# order by name, roles1, roles2;
#
# This gave output:
#
# +------------------------------------------+
# | name           | roles1  | roles2        |
# +------------------------------------------+
# | "Keanu Reeves" | ["Neo"] | ["John Wick"] |
# +------------------------------------------+
#

def get_movie_by_title (str): 
    # initialise output movie 
    the_movie = {} 
    # iterate through all the keys of the movie dictionary 
    # looking for one with the right title 
    for movie_id in movies.keys():
        if movies[movie_id]['title'] == str:
            the_movie = movies[movie_id]
            break
    return the_movie 

title1    = sys.argv[2] 
title2    = sys.argv[3]

movie1 = get_movie_by_title(title1)
movie2 = get_movie_by_title(title2)

for actor1 in movie1['actors']:
    for actor2 in movie2['actors']:  
        if actor1['person_id'] == actor2['person_id']:
            roles1 = actor1['roles']
            roles2 = actor2['roles']
            for r1 in roles1:
                for r2 in roles2:
                    print ("Actor %s plays %s in %s and %s in %s" % (actor1['name'], r1, title1, r2, title2))
            
