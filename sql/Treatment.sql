drop table if exists Treatment; 

CREATE TABLE Treatment (
   treatmentID integer,
   name varchar(20),
   isMedication bit, -- 1 for medication, 0 for procedure
   PRIMARY KEY (treatmentID)
);
