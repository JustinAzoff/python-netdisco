#!/bin/sh -x 
export NETDISCO_DB_CFG=tests/db.cfg
rm tests/test.db || true
sqlite3 tests/test.db < tests/test.db.sql
nosetests --with-xunit $*
