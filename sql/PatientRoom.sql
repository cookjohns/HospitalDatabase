drop table if exists PatientRoom; 

CREATE TABLE PatientRoom (
   roomNumber integer,
   patientID integer,
   PRIMARY KEY (roomNumber),
   FOREIGN KEY (patientID) REFERENCES Patient (patientID)
);
