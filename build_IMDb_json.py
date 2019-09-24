import json
import csv
import pickle
import os
 
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

genres = {}

with open('IMDb_relational/has_genre.dsv', mode='r') as csvfile:
    genresCSV = csv.DictReader(csvfile, delimiter='|')
    for row in genresCSV:
        genre = row["genre"]
        if row["movie_id"] in genres.keys():
            l = genres[row["movie_id"]]
        else:
            l = []
        l.append(genre) 
        genres[row["movie_id"]] = l             

for movie_id in movies.keys():
    if movie_id in genres.keys():
        m = movies[movie_id]
        m["genres"] = genres[movie_id]

plays_role = {}

with open('IMDb_relational/plays_role.dsv', mode='r') as csvfile:
    rolesCSV = csv.DictReader(csvfile, delimiter='|')
    for row in rolesCSV:
        role = row["role"]
        key = row["movie_id"] + "," + row["person_id"]
        if key in plays_role.keys():
            l = plays_role[key]
        else:
            l = []
        l.append(role) 
        plays_role[key] = l             

actors = {}
directors = {}
producers = {}
writers = {}

with open('IMDb_relational/has_position.dsv', mode='r') as csvfile: 
    creditsCSV = csv.DictReader(csvfile, delimiter='|')
    for row in creditsCSV:
        c         = row["position"]
        movie_id  = row["movie_id"]
        person_id = row["person_id"]
        _person = people[person_id]
        person = _person.copy()
        if c == 'actor':
            roles_key = movie_id + "," + person_id
            if roles_key in plays_role.keys():
                person["roles"] = plays_role[roles_key]
            if movie_id in actors.keys():
                l = actors[movie_id]
            else:
                l = []
            l.append(person)
            actors[movie_id] = l 
        elif c == 'director':
            if movie_id in directors.keys():
                l = directors[movie_id]            
            else:
                l = []
            l.append(person)
            directors[movie_id] = l 
        elif c == 'writer':
            if movie_id in writers.keys():
                l = writers[movie_id]
            else:
                l = []
            l.append(person)
            writers[movie_id] = l 
        elif c == 'producer':            
            if movie_id in producers.keys():
                l = producers[movie_id]
            else:
                l = []
            l.append(person)
            producers[movie_id] = l 

movies_copy = movies.copy()         
            
for movie_id in movies.keys():
    m = movies[movie_id]
    if movie_id in actors.keys():
        m["actors"] = actors[movie_id]
    if movie_id in writers.keys():
        m["writers"] = writers[movie_id]
    if movie_id in directors.keys():
        m["directors"] = directors[movie_id]
    if movie_id in producers.keys():
        m["producers"] = producers[movie_id]


acted_in = {}
directed = {}
produced = {}
wrote_for = {}

with open('IMDb_relational/has_position.dsv', mode='r') as csvfile: 
    creditsCSV = csv.DictReader(csvfile, delimiter='|')
    for row in creditsCSV:
        c         = row["position"]
        movie_id  = row["movie_id"]
        person_id = row["person_id"]
        movie = movies_copy[movie_id]
        if c == 'actor':
            roles_key = movie_id + "," + person_id
            if roles_key in plays_role.keys():
                movie["roles"] = plays_role[roles_key]
            if person_id in acted_in.keys():
                l = acted_in[person_id]
            else:
                l = []
            l.append(movie)
            acted_in[person_id] = l 
        elif c == 'director':
            if person_id in directed.keys():
                l = directed[person_id]            
            else:
                l = []
            l.append(movie)
            directed[person_id] = l 
        elif c == 'writer':
            if person_id in wrote_for.keys():
                l = wrote_for[person_id]
            else:
                l = []
            l.append(movie)
            wrote_for[person_id] = l 
        elif c == 'producer':            
            if person_id in produced.keys():
                l = produced[person_id]
            else:
                l = []
            l.append(movie)
            produced[person_id] = l 

for person_id in people.keys():
    p = people[person_id]
    if person_id in acted_in.keys():
        p["acted_in"] = acted_in[person_id]
    if person_id in wrote_for.keys():
        p["wrote_for"] = wrote_for[person_id]
    if person_id in directed.keys():
        p["directed"] = directed[person_id]
    if person_id in produced.keys():
        p["produced"] = produced[person_id]


# create target dir if it does not exist
target_dir = 'DOCtorWho/data/' 
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
    print("Creating directory " , target_dir ,  " ...")
        
movies_file_path = target_dir + 'movies.pickled'         
if os.path.exists(movies_file_path):
    os.remove(movies_file_path)

people_file_path = target_dir + 'people.pickled'    
if os.path.exists(people_file_path):
    os.remove(people_file_path)
  
with open(movies_file_path, mode= "wb") as moviesFile:
    pickle.dump(movies, moviesFile)

with open(people_file_path, mode= "wb") as peopleFile:
    pickle.dump(people, peopleFile)
    
        

