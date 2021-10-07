#!/bin/sh
cat $1 | ${NEO4JBINPATH}/cypher-shell -a bolt://localhost:7687 -u neo4j -p db1a --format verbose | head -n-2

