September 2020.
Timothy G. Griffin
University of Cambridge
tgg22@cam.ac.uk

This project contains scripts to 
construct three database instances from IMDb data
to be used in database lectures at the University of Cambridge.

These scripts will 

1) download data files from https://datasets.imdbws.com
2) filter the results of (1) 
3) contruct an HyperSQL instance 
4) contruct a Neo4j instance 
5) construct a DOCtor Who instance
   (where DOCtor Who is a simple json-based "database" built using python dictionaries)

I assume you are using some flavour of Unix.
Note on python: I'm currently using python3.5, but the python scripts
should work with just about any version. 

Instructions for constructing databases 

0) in a shell, do a ". set_env_vars" to set environment variables. 
   This will set 
    HSQLDBPATH    : path to hsqldb-<version>/hsqldb/lib 
    NEO4JBINPATH  : path to neo4j-community-<version>/bin 
    NEO4JDATAPATH : path to neo4j-community-<version>/data/databases 

========== relational =================

1) run "python3.5 build_IMDb_raw.py"
   This will fetch IMDb *.tsv.gz data files into IMDb_raw from https://datasets.imdbws.com (See IMDb_access.txt)
   and then uncompress them.

2) run "python3.5 build_IMDb_relational.py" 
   This creates the directory IMDb_relational/ and places *.dsv files in it. 
   Read comments in build_IMDb_relational.py.  In particular, I have had
   problems with unclosed quotes in the title.akas.tsv file which required
   deleting some lines by hand. 

3) run script hsqldb_load.sh
   This invokes HyperSql to execute hsqldb_load.sql, creating database
   from the *.dsv files in IMDb_relational.

NOTE: there are two useful scripts for testing:

hsqldb_gui.sh : pops up a (shabby) GUI interface for the relational database
hsqldb_shell.sh : starts a interactive shell for the relational database

========== document "database" =================

6) run "python3.5 build_IMDb_json.py" 
   This creates DOCtorWho/data/movies.pickled and DOCtorWho/data/people.pickled
   from IMDb_relational/*.dsv files.

NOTE: several query example files are provided in DOCtorWho/*py

========== graph database =================

4) run "python3.5 build_IMDb_graph.py" 
   This creates *.dsv files in IMDb_graph/ from files in IMDb_relational/

5) run neo4j_load.sh
   Neo4j database created ing $NEO4JDATAPATH/graph-db/

NOTE: for cypher documentation see https://neo4j.com/docs/cypher-manual/current

========== TO DO SOMEDAY =================

1) learn how to write python code ;-) 
2) modify scripts  so that they read *.tsv.gz files directly) 
3) make code more robust wrt errors in the *.tsv files (like unmatched quotes)
4) 