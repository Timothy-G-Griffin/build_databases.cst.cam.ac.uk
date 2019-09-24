
drop view  if exists romcom_ids; 
drop table if exists genres;
drop table if exists credits;

drop table if exists has_genre;
drop table if exists has_position;
drop table if exists plays_role;
drop table if exists people;
drop table if exists movies;

-- create tables for movie database

-- movies

CREATE TABLE movies (
movie_id varchar(16) PRIMARY KEY,
title varchar(255) NOT NULL,
year integer,
type varchar(16) NOT NULL,
minutes integer, 
rating double,
votes integer 
); 

-- people

CREATE TABLE people (
person_id varchar(16) PRIMARY KEY,
name varchar(255) NOT NULL,
birthYear integer,
deathYear integer
); 

-- credits

CREATE TABLE has_position (
person_id  varchar(16) NOT NULL REFERENCES people (person_id), 
movie_id  varchar(16) NOT NULL REFERENCES movies (movie_id), 
position varchar(255) NOT NULL,
PRIMARY KEY (person_id, movie_id) 
); 

-- roles



CREATE TABLE plays_role (
person_id varchar(16) NOT NULL REFERENCES people (person_id), 
movie_id varchar(16) NOT NULL REFERENCES movies (movie_id), 
role varchar(255) NOT NULL,
PRIMARY KEY (person_id, movie_id, role) 
); 


-- genres

create table has_genre (
   movie_id varchar(16) NOT NULL,
   genre varchar(100) NOT NULL,
   PRIMARY KEY (movie_id, genre)    
);

commit;

-- import rows from dsv files 

* *DSV_COL_SPLITTER = \|

* *DSV_TARGET_TABLE = movies 

\m IMDb_relational/movies.dsv

commit; 

* *DSV_TARGET_TABLE = people

\m IMDb_relational/people.dsv

commit; 

* *DSV_TARGET_TABLE = has_genre

\m IMDb_relational/has_genre.dsv

commit; 

* *DSV_TARGET_TABLE = has_position

\m IMDb_relational/has_position.dsv

commit; 

* *DSV_TARGET_TABLE = plays_role

\m IMDb_relational/plays_role.dsv

commit; 





