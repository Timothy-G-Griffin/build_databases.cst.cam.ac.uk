-- remove views

drop view if exists bacon_numbers;
drop view if exists bacon_number_9;
drop view if exists bacon_number_8;
drop view if exists bacon_number_7;
drop view if exists bacon_number_6;
drop view if exists bacon_number_5;
drop view if exists bacon_number_4;
drop view if exists bacon_number_3;
drop view if exists bacon_number_2;
drop view if exists bacon_number_1;
drop view if exists coactors;
drop view if exists acts_in;
drop view if exists produced;
drop view if exists wrote;
drop view if exists directed;
drop view if exists is_self;
drop view if exists romcom_ids;

-- remove relationships first! 
drop table if exists has_alternative;
drop table if exists has_genre;
drop table if exists has_position;
drop table if exists plays_role;

-- remove entity sets
drop table if exists countries;
drop table if exists languages;
drop table if exists genres;
drop table if exists people;
drop table if exists movies;


-- create tables for movie database

SET DEFAULT TABLE TYPE CACHED

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


CREATE TABLE languages (
code varchar(3) PRIMARY KEY,
name varchar(255) NOT NULL 
); 

CREATE TABLE countries (
code varchar(4) PRIMARY KEY,
name varchar(255) NOT NULL 
); 

CREATE TABLE has_alternative (
movie_id  varchar(16) NOT NULL REFERENCES movies (movie_id), 
alt_id integer NOT NULL,
title varchar(255) NOT NULL,
country_code varchar(4) REFERENCES countries (code), 
language_code varchar(3) REFERENCES languages (code), 
--country_code varchar(4), 
--language_code varchar(3), 
is_original boolean,
PRIMARY KEY (movie_id, alt_id) 
);

-- has_position 
-- note: column 'position' should really be a part of
-- the key.  But current IMDb data has only one position
-- per (person_id, movie_id). Grrr. 
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

create table genres (
   genre_id integer NOT NULL,
   genre varchar(100) NOT NULL,
   PRIMARY KEY (genre_id)    
);

create table has_genre (
   movie_id varchar(16) NOT NULL REFERENCES movies (movie_id), 
   genre_id integer NOT NULL REFERENCES genres (genre_id), 
   PRIMARY KEY (movie_id, genre_id)    
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

* *DSV_TARGET_TABLE = genres

\m IMDb_relational/genres.dsv

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

* *DSV_TARGET_TABLE = countries

\m IMDb_relational/country.dsv

commit; 

* *DSV_TARGET_TABLE = languages

\m IMDb_relational/language.dsv

commit; 

-- this next line is needed for varchar columns to say that
-- and empty string should be treated as null by the importer.
-- See http://hsqldb.org/doc/2.0/util-guide/sqltool-chapt.html#sqltool_csv-sect
* *NULL_REP_TOKEN =

* *DSV_TARGET_TABLE = has_alternative

\m IMDb_relational/has_alternative.dsv

commit; 

-- create views

create view romcom_ids as
    select m.movie_id as movie_id
    from movies as m
    join has_genre as hg1 on hg1.movie_id = m.movie_id
    join has_genre as hg2 on hg2.movie_id = m.movie_id
    join genres as g1 on g1.genre_id = hg1.genre_id
    join genres as g2 on g2.genre_id = hg2.genre_id
    where g1.genre = 'Romance' and g2.genre = 'Comedy';


create view acts_in as 
   select person_id, movie_id
   from has_position
   where position = 'actor'; 

create view produced as 
   select person_id, movie_id
   from has_position
   where position = 'producer'; 

create view wrote as 
   select person_id, movie_id
   from has_position
   where position = 'writer'; 

create view directed as 
   select person_id, movie_id
   from has_position
   where position = 'director'; 

create view is_self as 
   select person_id, movie_id
   from has_position
   where position = 'self'; 

create view coactors as 
  select distinct p1.person_id as pid1, 
                  p2.person_id as pid2
  from plays_role as p1 
  join plays_role as p2 on p2.movie_id = p1.movie_id; 

create view bacon_number_1 as 
  select distinct pid2 as pid, 
                  1 as bacon_number 
  from coactors 
  where pid1 = 'nm0000102' and pid1 <> pid2; 

create view bacon_number_2 as 
  select distinct ca.pid2 as pid, 
                  2 as bacon_number 
  from bacon_number_1 as bn1
  join coactors as ca on ca.pid1 = bn1.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1));

create view bacon_number_3 as 
  select distinct ca.pid2 as pid, 
                  3 as bacon_number 
  from bacon_number_2 as bn2
  join coactors as ca on ca.pid1 = bn2.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2));

create view bacon_number_4 as 
  select distinct ca.pid2 as pid, 
                  4 as bacon_number 
  from bacon_number_3 as bn3
  join coactors as ca on ca.pid1 = bn3.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2))
  and not(ca.pid2 in (select pid from bacon_number_3));
  

create view bacon_number_5 as 
  select distinct ca.pid2 as pid, 
                  5 as bacon_number 
  from bacon_number_4 as bn4
  join coactors as ca on ca.pid1 = bn4.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2))
  and not(ca.pid2 in (select pid from bacon_number_3))
  and not(ca.pid2 in (select pid from bacon_number_4));
  

create view bacon_number_6 as 
  select distinct ca.pid2 as pid, 
                  6 as bacon_number 
  from bacon_number_5 as bn5
  join coactors as ca on ca.pid1 = bn5.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2))
  and not(ca.pid2 in (select pid from bacon_number_3))
  and not(ca.pid2 in (select pid from bacon_number_4))
  and not(ca.pid2 in (select pid from bacon_number_5));

create view bacon_number_7 as 
  select distinct ca.pid2 as pid, 
                  7 as bacon_number 
  from bacon_number_6 as bn6
  join coactors as ca on ca.pid1 = bn6.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2))
  and not(ca.pid2 in (select pid from bacon_number_3))
  and not(ca.pid2 in (select pid from bacon_number_4))
  and not(ca.pid2 in (select pid from bacon_number_5))
  and not(ca.pid2 in (select pid from bacon_number_6));


create view bacon_number_8 as 
  select distinct ca.pid2 as pid, 
                  8 as bacon_number 
  from bacon_number_7 as bn7
  join coactors as ca on ca.pid1 = bn7.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2))
  and not(ca.pid2 in (select pid from bacon_number_3))
  and not(ca.pid2 in (select pid from bacon_number_4))
  and not(ca.pid2 in (select pid from bacon_number_5))
  and not(ca.pid2 in (select pid from bacon_number_6))
  and not(ca.pid2 in (select pid from bacon_number_7));

create view bacon_number_9 as 
  select distinct ca.pid2 as pid, 
                  9 as bacon_number 
  from bacon_number_8 as bn8
  join coactors as ca on ca.pid1 = bn8.pid 
  where ca.pid2 <> 'nm0000102' 
  and not(ca.pid2 in (select pid from bacon_number_1))
  and not(ca.pid2 in (select pid from bacon_number_2))
  and not(ca.pid2 in (select pid from bacon_number_3))
  and not(ca.pid2 in (select pid from bacon_number_4))
  and not(ca.pid2 in (select pid from bacon_number_5))
  and not(ca.pid2 in (select pid from bacon_number_6))
  and not(ca.pid2 in (select pid from bacon_number_7))
  and not(ca.pid2 in (select pid from bacon_number_8));  

create view bacon_numbers as 
   select * from bacon_number_1
   union 
   select * from bacon_number_2 
   union 
   select * from bacon_number_3 
   union 
   select * from bacon_number_4 
   union 
   select * from bacon_number_5 
   union 
   select * from bacon_number_6 
   union 
   select * from bacon_number_7 
   union 
   select * from bacon_number_8 
   union 
   select * from bacon_number_9 ;   

commit;




