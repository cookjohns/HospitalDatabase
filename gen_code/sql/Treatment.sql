drop table if exists Treatment; 

create table Treatment (
   treatmentID integer,
   name varchar(20),
   isMedication bit, // return 1 for medication, 0 for procedure
   PRIMARY KEY (treatmentID)
);
