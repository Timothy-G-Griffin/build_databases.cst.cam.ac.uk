import csv

# build_IMDb_graph.py

my_delimiter      = "|"

movies_in_file   = "IMDb_relational/movies.dsv"
people_in_file   = "IMDb_relational/people.dsv"
genres_in_file   = "IMDb_relational/genres.dsv"
roles_in_file    = "IMDb_relational/plays_role.dsv"
credits_in_file  = "IMDb_relational/credits.dsv"


movies_out_file   = "IMDb_graph/movies.dsv"
people_out_file   = "IMDb_graph/people.dsv"
acted_in_out_file = "IMDb_graph/acted_in.dsv"
directed_out_file = "IMDb_graph/directed.dsv"
produced_out_file = "IMDb_graph/produced.dsv"
wrote_out_file    = "IMDb_graph/wrote.dsv"

genres_map = {}

with open(genres_in_file, mode='r') as g_in:
    genresCSV = csv.DictReader(g_in, delimiter='|')
    for row in genresCSV:
        genre = row["genre"]
        if row["movie_id"] in genres_map.keys():
            l = genres_map[row["movie_id"]]
        else:
            l = []
        l.append(genre) 
        genres_map[row["movie_id"]] = l

    
with open(movies_in_file, "r") as m_in:
    moviesCSV = csv.DictReader(m_in, delimiter=my_delimiter)    
    with open(movies_out_file, "w") as m_out:
        # write header
        header = my_delimiter.join(["movie_id:ID",
                                    "title:string",
                                    "year:int",
                                    "type:string",
                                    "minutes:int",
                                    "rating:float",
                                    "votes:int",
                                    "genres:string[]",
                                    ":LABEL"])
        print (header, file=m_out)
        # write out records  
        for row in moviesCSV:
            movie_id = row["movie_id"]
            if movie_id in genres_map.keys():
                genres = genres_map[movie_id]
                genres_str = ";".join(genres)
            else:
                genres_str = ""
            row_out = my_delimiter.join([movie_id,
                                         row["title"],
                                         row["year"],
                                         row["type"],
                                         row["minutes"],
                                         row["rating"],
                                         row["votes"],
                                         genres_str, 
                                         "Movie"])
            print (row_out, file=m_out)

with open(people_in_file, "r") as p_in:
    peopleCSV = csv.DictReader(p_in, delimiter=my_delimiter)    
    with open(people_out_file, "w") as p_out:
        # write header
        header = my_delimiter.join(["person_id:ID", "name:string", "birthYear:int", "deathYear:int", ":LABEL"])
        print (header, file=p_out)
        # write out records  
        for row in peopleCSV:
            row_out = my_delimiter.join([row["person_id"], row["name"], row["birthYear"], row["deathYear"], "Person"])
            print (row_out, file=p_out)

            
plays_role = {}

with open(roles_in_file, mode='r') as r_in:
    rolesCSV = csv.DictReader(r_in, delimiter='|')
    for row in rolesCSV:
        role = row["role"]
        key = row["movie_id"] + "," + row["person_id"]
        if key in plays_role.keys():
            l = plays_role[key]
        else:
            l = []
        l.append(role) 
        plays_role[key] = l

acted_in_out = open(acted_in_out_file, "w")
directed_out = open(directed_out_file, "w")
produced_out = open(produced_out_file, "w")
wrote_out    = open(wrote_out_file, "w")

#write headers
acted_in_header = my_delimiter.join([":START_ID", ":END_ID", "roles:string[]", ":TYPE"])
print (acted_in_header, file=acted_in_out) 

directed_header = my_delimiter.join([":START_ID", ":END_ID", ":TYPE"])
print (directed_header, file=directed_out)

produced_header = my_delimiter.join([":START_ID", ":END_ID", ":TYPE"])
print (produced_header, file=produced_out)

wrote_header = my_delimiter.join([":START_ID", ":END_ID", ":TYPE"])
print (wrote_header, file=wrote_out) 

with open(credits_in_file, mode='r') as c_in: 
    creditsCSV = csv.DictReader(c_in, delimiter=my_delimiter)
    for row in creditsCSV:
        c         = row["category"]
        movie_id  = row["movie_id"]
        person_id = row["person_id"]
        if c == 'actor':
            roles_key = movie_id + "," + person_id
            if roles_key in plays_role.keys():
                roles = plays_role[roles_key]
                roles_str = ";".join(roles)
            else:
                roles_str = ""
            acted_in = my_delimiter.join([person_id, movie_id, roles_str, "ACTED_IN"])
            print(acted_in, file=acted_in_out)
        elif c == 'director':
            directed = my_delimiter.join([person_id, movie_id, "DIRECTED"])
            print(directed, file=directed_out)
        elif c == 'writer':
            writes = my_delimiter.join([person_id, movie_id, "WROTE"])            
            print(writes, file=wrote_out)
        elif c == 'producer':
            produced = my_delimiter.join([person_id, movie_id, "PRODUCED"])                        
            print(produced, file=produced_out)
