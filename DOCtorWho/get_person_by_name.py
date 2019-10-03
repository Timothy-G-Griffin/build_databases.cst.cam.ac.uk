import sys     
import os.path 
import pickle  
import pprint
import json 

data_dir = sys.argv[1] # directory of data 
name     = sys.argv[2] # a person's name 

# use os.path.join so that path works on both Windows and Unix 
people_path = os.path.join(data_dir, 'people.pickled')

# open the people dictionary file and un-pickle it 
peopleFile = open(people_path, mode= "rb")
people = pickle.load(peopleFile)

pprint.pprint (people)

# initialise output person
the_person = {} 

# iterate through all the keys of the people dictionary 
# looking for one with the right name
for person_id in people.keys():
    if people[person_id]['name'] == name:
        the_person = people[person_id]
        break 
  
pprint.pprint (the_person)


