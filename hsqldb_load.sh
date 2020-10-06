#!/bin/bash
#
# for setting the java system property REMOVE_EMPTY_VARS
# see http://hsqldb.org/doc/2.0/util-guide/sqltool-chapt.html#sqltool_csv-sect
#
java -jar -DREMOVE_EMPTY_VARS='false' $HSQLDBPATH/sqltool.jar --rcfile=sqltool.rc db1a hsqldb_load.sql
