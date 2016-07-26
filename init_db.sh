rm ./HospitalDB.db 
rm ./gen_code/src/output.sql
(cd ./gen_code/src/
 node main.js)
cat ./sql/*|sqlite3 HospitalDB.db
cat ./gen_code/src/output.sql|sqlite3 HospitalDB.db
