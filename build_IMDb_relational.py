
import csv 
import os
import iso3166 # for country names 
import iso639  # for language names 
#	       
# build_IMDb_relational.py
#
# Assumes directory IMDb_raw contains files downloaded from https://datasets.imdbws.com/
# and uncommpressed:
# 
# name.basics.tsv
# title.akas.tsv
# title.basics.tsv
# title.crew.tsv
# title.episode.tsv
# title.principals.tsv
# title.ratings.tsv
# Check www.imdb.com/interfaces for possible changes to files or file formats
#
# On September 7 2020 the line counts for these files were
# 10342842 name.basics.tsv
# 23332150 title.akas.tsv
#  7142835 title.basics.tsv
#  7142835 title.crew.tsv
#  5128103 title.episode.tsv
# 40990137 title.principals.tsv
#  1070628 title.ratings.tsv
# 95149530 total

# We can see the types of the titles (titleType column):
# cut -f 2 title.basics.tsv | sort | uniq -c | sort -n
#       1 titleType
#   13145 tvShort
#   26254 videoGame
#   29538 tvSpecial
#   33163 tvMiniSeries
#  123384 tvMovie
#  191700 tvSeries
#  277756 video
#  560373 movie
#  759375 short
# 5128146 tvEpisode

# In order to make database that students can explore even on a low-powered laptop, we
# will filter out much of this data.
# Running this script will select all movies (movie or tvMovie) between years start-year end-year (inclusive) that have
# ratings not lower than rating-cutoff with at least votes-needed number of votes.
# Adult titles will be excluded.
# 
# It will generate files in IMDb_relational: 
#    movies.tsv   
#    people.tsv
#    has_position.tsv
#    plays_role.tsv
#    has_genre.tsv
#    genres.tsv 
#
# We want recent movies: 
start_year     = 2000
end_year       = 2021
# cut offs tuned to get around 1000 movies in total 
rating_cutfoff = 7
votes_needed_for_movie   = 50000
votes_needed_for_tvmovie = 1000

bar      = "|"
source_dir = "IMDb_raw/" 
target_dir = "IMDb_relational/"

movies_in_file     = source_dir + "title.basics.tsv"
ratings_in_file    = source_dir + "title.ratings.tsv"
positions_in_file  = source_dir + "title.principals.tsv"
people_in_file     = source_dir + "name.basics.tsv"
alternative_title_in_file = source_dir + "title.akas.tsv"

movies_out_file     = target_dir + "movies.dsv"
has_genre_out_file = target_dir + "has_genre.dsv"
genres_out_file     = target_dir + "genres.dsv"
positions_out_file  = target_dir + "has_position.dsv";
roles_out_file      = target_dir + "plays_role.dsv";
people_out_file     = target_dir + "people.dsv"
language_out_file   = target_dir + "language.dsv"
country_out_file    = target_dir + "country.dsv"
has_alternative_title_out_file = target_dir + "has_alternative.dsv"

# these codes some to be missing form the iso639 module 
fix_iso639 = {}
fix_iso639['cmn'] = 'Mandarin Chinese'
fix_iso639['qbp'] = 'ISO-639 Reserved for local use'
fix_iso639['qbn'] = 'ISO-639 Reserved for local use'
fix_iso639['yue'] = 'Yue Chinese'

# create target dir if it does not exist         
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
    print("Creating directory " , target_dir ,  " ...")

    
print("... filtering movies ...");
# title.basics.tsv - Contains the following information for titles:
# ----------------------------------------------------------------------
# tconst (string)        - alphanumeric unique identifier of the title
# titleType (string)     – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
# primaryTitle (string)  – the more popular title / the title used by the filmmakers on promotional materials at the point of release
# originalTitle (string) - original title, in the original language
# isAdult (boolean)      - 0: non-adult title; 1: adult title
# startYear (YYYY)       – represents the release year of a title. In the case of TV Series, it is the series start year
# endYear (YYYY)         – TV Series end year. ‘\N’ for all other title types
# runtimeMinutes         – primary runtime of the title, in minutes
# genres (string array)  – includes up to three genres associated with the title

movies = {}


with open(movies_in_file, mode='r') as csvfile:
    moviesCSV = csv.DictReader(csvfile, delimiter='\t')
    for line in moviesCSV:
        # note that int(line['startYear']) can fail when line['startYear'] is '\N' (null) 
        try: 
            if (     ((line['titleType'] == 'movie') or (line['titleType'] == 'tvMovie'))
                 and (int(line['isAdult']) == 0)
                 and (int(line['startYear']) >= start_year)
                 and (end_year >= int(line['startYear'], 10))): 
                movies[line['tconst'] + bar + 'primaryTitle'] = line['primaryTitle']
                movies[line['tconst'] + bar + 'year']         = line['startYear']
                movies[line['tconst'] + bar + 'genres']       = line['genres']
                movies[line['tconst'] + bar + 'type']         = line['titleType']
                if line['runtimeMinutes'] != '\\N': 
                    movies[line['tconst'] + bar + 'minutes']  = line['runtimeMinutes']
                else:
                    movies[line['tconst'] + bar + 'minutes']  = ""
                mcount = mcount + 1
        except:
            pass 

print ("... processing ratings ...")
# title.ratings.tsv – Contains the IMDb rating and votes information for titles
# ------------------------------------------------------------------------------
# tconst (string) - alphanumeric unique identifier of the title
# averageRating   – weighted average of all the individual user ratings
# numVotes        - number of votes the title has received
#    

keep = {}
rate = {}

with open(ratings_in_file, mode='r') as csvfile:
    ratingsCSV = csv.DictReader(csvfile, delimiter='\t')
    for line in ratingsCSV:
        mkey = line['tconst'] + bar + 'type'
        if mkey in movies.keys():
            ttype = movies[mkey]
            votes = int(line['numVotes'], 10)
            if ((float(line['averageRating']) >= rating_cutfoff)
               and (   ((votes >= votes_needed_for_tvmovie) and (ttype == 'tvMovie'))
                    or ((votes >= votes_needed_for_movie) and (ttype == 'movie')))): 
                keep[line['tconst']] = 1
                rate[line['tconst'] + bar + 'averageRating'] = line['averageRating']
                rate[line['tconst'] + bar + 'numVotes']      = line['numVotes']            

print("... generating movies, genres ...")
movies_out     = open(movies_out_file, "w")
has_genre_out  = open(has_genre_out_file, "w")
genres_out     = open(genres_out_file, "w")
genre_to_id = {}
next_genre_id = 1 

# write headers 
print(bar.join(["movie_id","title", "year", "type", "minutes", "rating", "votes"]), file=movies_out)
print(bar.join(["movie_id", "genre_id"]), file=has_genre_out)
print(bar.join(["genre_id", "genre"]), file=genres_out)
for key in keep.keys(): 
    keyb = key + bar 
    print (
        bar.join([ 
        key,
	movies[keyb + 'primaryTitle'], 
	movies[keyb + 'year'],
	movies[keyb + 'type'],
        movies[keyb + 'minutes'],
	rate[keyb + 'averageRating'], 
	rate[keyb + 'numVotes']]),
        file=movies_out
    )
    genres = movies[keyb + 'genres']
    if genres != '\\N': 
       for g in genres.split(','):
           if g in genre_to_id.keys():
               print(bar.join([key, str(genre_to_id[g])]), file=has_genre_out)
           else:
               print(bar.join([key, str(next_genre_id)]), file=has_genre_out)               
               print(bar.join([str(next_genre_id), g]), file=genres_out)
               genre_to_id[g] = next_genre_id 
               next_genre_id = next_genre_id + 1


print("... processing alternative titles ...")
#
# title.akas.tsv - Contains the following information for titles:
# ----------------------------------------------------------------------
# titleId (string) - a tconst, an alphanumeric unique identifier of the title
# ordering (integer) – a number to uniquely identify rows for a given titleId
# title (string) – the localized title
# region (string) - the region for this version of the title
# language (string) - the language of the title
# types (array) - Enumerated set of attributes for this alternative title.
#                 One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". 
#                 New values may be added in the future without warning
# attributes (array) - Additional terms to describe this alternative title, not enumerated
# isOriginalTitle (boolean) – 0: not original title; 1: original title

has_alt_out = open(has_alternative_title_out_file, "w")
country = {}
language = {} 
rowkey = {}
# write header
print(bar.join(["movie_id", "alt_id", "title", "country_code", "language_code", "is_original"]), file=has_alt_out)
#
# Warning: Sometimes ththe file title.akas.tsv contains bugs like non-closed quotes.  Such things
# can cause DictReader to raise an exception.  Offending lines must then be removed by hand. 
#
with open(alternative_title_in_file, mode='r') as csvfile:
    altCSV = csv.DictReader(csvfile, delimiter='\t')
    try: 
        for line in altCSV:
            key = line['titleId']
            if key in keep.keys():
                country_code   = line['region']
                language_code = line['language']
                original = line['isOriginalTitle']            
                if (country_code == '\\N'):
                   country_code = ''                    
                else:
                    try:
                        country[country_code] = iso3166.countries.get(country_code).name
                    except:
                        country[country_code] = "Not an ISO-3166 country?"    # tgg22 : I was not able to fix these                                 
                if (language_code == '\\N'):
                     language_code = ''
                else:
                    try:
                        language[language_code] = iso639.find(language_code)['name']
                    except:
                        language[language_code] = fix_iso639[language_code] # "Not an ISO-639 language?"
                if (original == '\\N'):
                    original = '' 
                else:
                    if (original == "0"):
                        original = "false"
                    else:
                        original = "true"
                if key in rowkey.keys():
                    rowkey[key] = rowkey[key] + 1
                else:
                    rowkey[key] = 0 
                print(bar.join([key, str(rowkey[key]), line['title'], country_code, language_code, original]), file=has_alt_out)
                    
    except csv.Error as e:
        print('ERROR on line {}: {}'.format(altCSV.line_num, e))
        exit() 
               
language_out = open(language_out_file, "w")
country_out  = open(country_out_file, "w")
# write headers
print(bar.join(["code", "name"]), file=language_out)
print(bar.join(["code", "name"]), file=country_out)

for key in language.keys():
    print(bar.join([key, language[key]]), file=language_out)

for key in country.keys():
    print(bar.join([key, country[key]]), file=country_out)
    
               
print ("... processing positions, roles ...")
# 
# title.principals.tsv – Contains the principal cast/crew for titles
# ---------------------------------------------------------------------
# tconst (string)     - alphanumeric unique identifier of the title
# ordering (integer)  – a number to uniquely identify rows for a given titleId
# nconst (string)     - alphanumeric unique identifier of the name/person
# category (string)   - the category of job that person was in
# job (string)        - the specific job title if applicable, else '\N'
# characters (string) - the name of the character played if applicable, else '\N'
#
# current dataset contains the following categories, some will be ignored ...
#
# actor
# actress
# archive_footage
# archive_sound
# cinematographer
# composer
# director
# editor
# producer
# production_designer
# self
# writer
#

positions_out = open(positions_out_file, "w")
roles_out     = open(roles_out_file, "w")
# write headers
print (bar.join(["movie_id","person_id", "position"]), file=positions_out) 
print (bar.join(["movie_id", "person_id", "role"]), file=roles_out)
keep_person = {}

with open(positions_in_file, mode='r') as csvfile:
    positionsCSV = csv.DictReader(csvfile, delimiter='\t')
    for line in positionsCSV:
        mkey = line['tconst'] 
        pkey = line['nconst'] 	    
        if mkey in keep.keys(): 
            use_it = 0;
            category = line['category'] 
            if ((category == 'actor')    or (category == 'actress') or
                (category == 'director') or (category == 'producer') or
                (category == 'writer')     or (category == 'self')):  
                use_it = 1
            if (use_it == 1): # check if person exists?  IMDb data may be buggy ... Would cause foreign key violation when inserted into db
                new_category = category
                if (category == 'actress'):
                    new_category = "actor"
                print(bar.join([mkey, pkey, new_category]), file=positions_out)
                keep_person[pkey] = 1
                characters = line['characters']
                if (characters != '\\N'):  # ignore null entry 
		    # parse characters entry of the form ["role_1", "role_2", ... "role_k"].
		    # for each role_i create an entry in roles table.
                    # Note : roles may contain "," [which is why we can't use split. :-( ] and "\"", 
                    l = len(characters)
                    if ((characters[0:1] == "[") and (characters[l-1:l] == "]")):
                        role_list = []
                        in_role = 0
                        role = ""
                        last = ""; 
                        for i in range(1, l): 
                            c = characters[i:i+1]
                            if ((in_role == 0) and (c == "\"")):
                                in_role = 1
                            elif ((in_role == 1) and (c == "\"") and (last != "\\")):
                                in_role = 0
                            elif ((in_role == 0) and (c == ",")):
                                role_list.append(role)
                                role = ""
                            elif ((in_role == 0) and (c == "]")):
                                role_list.append(role)
                                role = ""
                            else:
                                role = role + c
                                last = c
                        for role in role_list: # check if there are duplicate roles in a characters? Could cause key violation when insert into db! 
                            print(bar.join([mkey, pkey, role]), file=roles_out) 



print("... processing people ...")
#
# name.basics.tsv.gz – Contains the following information for names:
# ------------------------------------------------------------------
# nconst (string)                      - alphanumeric unique identifier of the name/person
# primaryName (string)                 – name by which the person is most often credited
# birthYear                            – in YYYY format
# deathYear                            – in YYYY format if applicable, else '\N'
# primaryProfession (array of strings) – the top-3 professions of the person
# knownForTitles (array of tconsts)    – titles the person is known for
#    
people_out = open(people_out_file, "w")
# write header 
print(bar.join(["person_id", "name", "birthYear", "deathYear"]), file=people_out)
with open(people_in_file, mode='r') as csvfile:
    peopleCSV = csv.DictReader(csvfile, delimiter='\t')
    for line in peopleCSV:
        key = line['nconst']
        if key in keep_person.keys(): 
            birth_year = line['birthYear']
            death_year = line['deathYear']
            if (birth_year == '\\N'):
                birth_year = ''
            if (death_year == '\\N'):
                death_year = '' 
            print(bar.join([key, line['primaryName'], birth_year, death_year]), file=people_out)



print ("... DONE!")



# files not currently used: 

# title.crew.tsv – Contains the director and writer information for all the titles in IMDb. Fields include:
# ----------------------------------------------------------------------------------------------------------
# tconst (string) - alphanumeric unique identifier of the title
# directors (array of nconsts) - director(s) of the given title
# writers (array of nconsts) – writer(s) of the given title


# title.episode.tsv – Contains the tv episode information. Fields include:
# ---------------------------------------------------------------------------
# tconst (string) - alphanumeric identifier of episode
# parentTconst (string) - alphanumeric identifier of the parent TV Series
# seasonNumber (integer) – season number the episode belongs to
# episodeNumber (integer) – episode number of the tconst in the TV series


