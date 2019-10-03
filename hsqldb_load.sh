#!/bin/bash

java -jar $HSQLDBPATH/sqltool.jar --rcfile=sqltool.rc db1a hsqldb_load.sql
