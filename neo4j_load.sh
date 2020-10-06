#!/bin/sh

IMPORT="$NEO4JBINPATH/neo4j-admin import"
DSV_DIR="IMDb_graph"
TARGET="graph.db"

# set password of default user (neo4j) to neo4j 
#COMMAND1="$NEO4JBINPATH/neo4j-admin set-initial-password neo4j"

COMMAND2="$IMPORT --database=$TARGET --delimiter | --nodes $DSV_DIR/movies.dsv --nodes $DSV_DIR/people.dsv --relationships $DSV_DIR/directed.dsv --relationships $DSV_DIR/wrote.dsv --relationships $DSV_DIR/produced.dsv --relationships $DSV_DIR/acted_in.dsv"


# Make sure database is empty
rm -rf "$NEO4JDATAPATH/$TARGET"

#echo $COMMAND1
#$COMMAND1

echo $COMMAND2
$COMMAND2
