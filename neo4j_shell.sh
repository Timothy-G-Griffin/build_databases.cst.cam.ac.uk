#!/bin/sh
# go to http://localhost:7474/
COMMAND="$NEO4JBINPATH/cypher-shell -a bolt://localhost:7687 -u neo4j -p db1A"
echo $COMMAND
$COMMAND
