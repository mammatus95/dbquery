#!/bin/sh

sqlite3 cellmos.db <<'END_SQL'
.mode table
.tables
.output cellmos_test.txt
select cellid,date,center_long,center_lat,lightnings from cell where lightnings>600 order by lightnings;
END_SQL
