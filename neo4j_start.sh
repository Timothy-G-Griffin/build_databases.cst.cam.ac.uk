#!/bin/sh
# go to http://localhost:7474/
NEO4J="$NEO4JBINPATH/neo4j"
COMMAND="$NEO4J start" 
echo $COMMAND
$COMMAND
