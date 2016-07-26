rm ./HospitalDB.db 
cat ./sql/*|sqlite3 HospitalDB.db
cat ./gen_code/src/test.sql|sqlite3 HospitalDB.db
