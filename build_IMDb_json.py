import json
import csv
import pickle
import os
import pprint # for debugging 

# create target dir if it does not exist
target_dir = 'DOCtorWho/data/' 
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
    print("Creating directory " , target_dir ,  " ...")
    
# construct people dictionary

people = {} 

with open('IMDb_relational/people.dsv', mode='r') as csvfile:
    peopleCSV = csv.DictReader(csvfile, delimiter='|')
    for row in peopleCSV:
        person = {'person_id' : row['person_id'], 'name' : row['name']}
        if row['birthYear'] != '':
            person['birthYear'] = row['birthYear']
        if row['deathYear'] != '':
            person['deathYear'] = row['deathYear']            
        people[row["person_id"]] = person

movies = {}

with open('IMDb_relational/movies.dsv', mode='r') as csvfile:
    moviesCSV = csv.DictReader(csvfile, delimiter='|')
    for row in moviesCSV:
        movies[row["movie_id"]] = row

plays_role = {}

with open('IMDb_relational/plays_role.dsv', mode='r') as csvfile:
    rolesCSV = csv.DictReader(csvfile, delimiter='|')
    for row in rolesCSV:
        role = row["role"]
        person_id = row["person_id"]
        movie_id = row["movie_id"]
        key = person_id + "," + movie_id 
        if key in plays_role.keys():
            l = plays_role[key] 
        else:
            l = []
        l.append(role)
        plays_role[key] = l 

directed = {}
produced = {}
wrote = {}
selfies = {}

with open('IMDb_relational/has_position.dsv', mode='r') as csvfile: 
    creditsCSV = csv.DictReader(csvfile, delimiter='|')
    for row in creditsCSV:
        c         = row["position"]
        movie_id  = row["movie_id"]
        person_id = row["person_id"]
        key = person_id + "," + movie_id         
        if c == 'self':
            selfies[key] = 1
        elif c == 'director':
            directed[key] = 1
        elif c == 'writer':
            wrote[key] = 1
        elif c == 'producer':            
            produced[key] = 1

            
# complete the "join". 
# have to introduce people_final
# since iterating of keys of people
# while changing keys of people...

people_final = {} 

for person_id in people.keys():
    _person = people[person_id]
    person = _person.copy()                
    for movie_id in movies.keys():
        _movie = movies[movie_id]
        movie = {}
        # just grab the important bits 
        movie['movie_id'] = movie_id
        movie['title'] = _movie['title']
        movie['year'] = _movie['year']        
        key = person_id + "," + movie_id         
        if key in plays_role.keys():
            movie_copy = movie.copy()
            movie_copy['roles'] = plays_role[key]
            if 'acted_in' in person.keys(): 
                l = person['acted_in']
            else:
                l = []
            l.append(movie_copy)            
            person['acted_in'] = l
        if key in directed.keys():
            movie_copy = movie.copy()            
            if 'directed' in person.keys(): 
                l = person['directed']
            else:
                l = []
            l.append(movie_copy)            
            person['directed'] = l            
        if key in wrote.keys():
            movie_copy = movie.copy()            
            if 'wrote' in person.keys(): 
                l = person['wrote']
            else:
                l = []
            l.append(movie_copy)            
            person['wrote'] = l            
        if key in produced.keys():
            movie_copy = movie.copy()            
            if 'produced' in person.keys(): 
                l = person['produced']
            else:
                l = []
            l.append(movie_copy)            
            person['produced'] = l            
        if key in selfies.keys():
            movie_copy = movie.copy()            
            if 'was_self' in person.keys(): 
                l = person['was_self']
            else:
                l = []
            l.append(movie_copy)            
            person['was_self'] = l            
    people_final[person_id] = person

# testing ...     
# pprint.pprint (people_final['nm0000354']) # Matt Damon 
# pprint.pprint (people_final['nm2225369']) # Jennifer Lawrence
# pprint.pprint (people_final['nm0000229']) # Steven Spielberg
# pprint.pprint (people_final['nm1000113']) # Etan Cohen
# pprint.pprint (people_final['nm0031976']) # Judd Apatow

people_file_path = target_dir + 'people.pickled'    
if os.path.exists(people_file_path):
    os.remove(people_file_path)

with open(people_file_path, 'wb') as peopleFile:
    pickle.dump(people_final, peopleFile)
            

# construct movies dictionary


genres = {}

with open('IMDb_relational/genres.dsv', mode='r') as csvfile:
    genresCSV = csv.DictReader(csvfile, delimiter='|')
    for row in genresCSV:
        genres[row["genre_id"]] = row["genre"]

has_genres = {}

with open('IMDb_relational/has_genre.dsv', mode='r') as csvfile:
    has_genreCSV = csv.DictReader(csvfile, delimiter='|')
    for row in has_genreCSV:
        movie_id = row["movie_id"]        
        genre = genres[row["genre_id"]]
        if movie_id in has_genres.keys():
            l = has_genres[movie_id]
        else:
            l = []
        l.append(genre)
        has_genres[movie_id] = l 

movies_final = {} 

for movie_id in movies.keys():
    _movie = movies[movie_id]
    movie = _movie.copy()
    if movie_id in has_genres.keys():
        movie['genres'] = has_genres[movie_id]
    for person_id in people.keys():
        _person = people[person_id]
        person = {}
        # just grab the important bits 
        person['person_id'] = person_id
        person['name'] = _person['name']
        key = person_id + "," + movie_id         
        if key in plays_role.keys():
            person_copy = person.copy()
            person_copy['roles'] = plays_role[key]
            if 'actors' in movie.keys(): 
                l = movie['actors']
            else:
                l = []
            l.append(person_copy)            
            movie['actors'] = l
        if key in directed.keys():
            person_copy = person.copy()            
            if 'directors' in movie.keys(): 
                l = movie['directors']
            else:
                l = []
            l.append(person_copy)            
            movie['directors'] = l            
        if key in wrote.keys():
            person_copy = person.copy()            
            if 'writers' in movie.keys(): 
                l = movie['writers']
            else:
                l = []
            l.append(person_copy)            
            movie['writers'] = l            
        if key in produced.keys():
            person_copy = person.copy()            
            if 'producers' in movie.keys(): 
                l = movie['producers']
            else:
                l = []
            l.append(person_copy)            
            movie['producers'] = l            
        if key in selfies.keys():
            person_copy = person.copy()            
            if 'as_self' in movie.keys(): 
                l = movie['as_self']
            else:
                l = []
            l.append(person_copy)            
            movie['as_self'] = l            
    movies_final[movie_id] = movie

# testing     
pprint.pprint (movies_final['tt1045658']) # Silver Linings Playbook


movies_file_path = target_dir + 'movies.pickled'         
if os.path.exists(movies_file_path):
    os.remove(movies_file_path)
    
with open(movies_file_path, mode= "wb") as moviesFile:
    pickle.dump(movies_final, moviesFile)


    
        

